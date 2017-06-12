
#include "smithlab_utils.hpp"
#include "smithlab_os.hpp"
#include "GenomicRegion.hpp"
#include "OptionParser.hpp"
#include "TwoStateHMM.hpp"

#include <numeric>
#include <cmath>
#include <fstream>
#include <iomanip>

#include <unistd.h>

using std::string;
using std::vector;
using std::cout;
using std::endl;
using std::cerr;
using std::numeric_limits;
using std::max;
using std::min;
using std::pair;

double
get_fdr_cutoff(const vector<double> &scores, const double fdr) {
  if (fdr <= 0)
    return numeric_limits<double>::max();
  else if (fdr > 1)
    return numeric_limits<double>::min();
  vector<double> local(scores);
  std::sort(local.begin(), local.end());
  size_t i = 0;
  for (; i < local.size() - 1 && 
         local[i+1] < fdr*static_cast<double>(i+1)/local.size(); ++i);
  return local[i];
}


static void
get_domain_scores(const vector<bool> &classes,
                  const vector<pair<double, double> > &meth,
                  const vector<size_t> &reset_points,
                  vector<double> &scores) {
  static const bool CLASS_ID = true;
  size_t n_cpgs = 0, reset_idx = 1;
  bool in_domain = false;
  double score = 0;
  for (size_t i = 0; i < classes.size(); ++i) {
    if (reset_points[reset_idx] == i) {
      if (in_domain) {
        in_domain = false;
        scores.push_back(score);
        score = 0;
      }
      ++reset_idx;
    }
    if (classes[i] == CLASS_ID) {
      in_domain = true;
      score += 1.0 - (meth[i].first/(meth[i].first + meth[i].second));
      ++n_cpgs;
    }
    else if (in_domain) {
      in_domain = false;
      scores.push_back(score);
      score = 0;
    }
  }
}


static void
build_domains(const bool VERBOSE, 
              const vector<SimpleGenomicRegion> &cpgs,
              const vector<double> &post_scores,
              const vector<size_t> &reset_points,
              const vector<bool> &classes,
              vector<GenomicRegion> &domains) {
  static const bool CLASS_ID = true;
  size_t n_cpgs = 0, n_domains = 0, reset_idx = 1, prev_end = 0;
  bool in_domain = false;
  double score = 0;
  for (size_t i = 0; i < classes.size(); ++i) {
    if (reset_points[reset_idx] == i) {
      if (in_domain) {
        in_domain = false;
        domains.back().set_end(prev_end);
        domains.back().set_score(n_cpgs);
        n_cpgs = 0;
        score = 0;
      }
      ++reset_idx;
    }
    if (classes[i] == CLASS_ID) {
      if (!in_domain) {
        in_domain = true;
        domains.push_back(GenomicRegion(cpgs[i]));
        domains.back().set_name("HYPO" + toa(n_domains++));
      }
      ++n_cpgs;
      score += post_scores[i];
    }
    else if (in_domain) {
      in_domain = false;
      domains.back().set_end(prev_end);
      domains.back().set_score(n_cpgs);
      n_cpgs = 0;
      score = 0;
    }
    prev_end = cpgs[i].get_end();
  }
  // Do we miss the final domain?????
}


template <class T, class U> static void
separate_regions(const bool VERBOSE, const size_t desert_size, 
                 vector<SimpleGenomicRegion> &cpgs,
                 vector<T> &meth, vector<U> &reads,
                 vector<size_t> &reset_points) {
  if (VERBOSE)
    cerr << "[SEPARATING BY CPG DESERT]" << endl;
  // eliminate the zero-read cpgs
  size_t j = 0;
  for (size_t i = 0; i < cpgs.size(); ++i)
    if (reads[i] > 0) {
      cpgs[j] = cpgs[i];
      meth[j] = meth[i];
      reads[j] = reads[i];
      ++j;
    }
  cpgs.erase(cpgs.begin() + j, cpgs.end());
  meth.erase(meth.begin() + j, meth.end());
  reads.erase(reads.begin() + j, reads.end());
  
  // segregate cpgs
  size_t prev_cpg = 0;
  for (size_t i = 0; i < cpgs.size(); ++i) {
    const size_t dist = (i > 0 && cpgs[i].same_chrom(cpgs[i - 1])) ? 
      cpgs[i].get_start() - prev_cpg : numeric_limits<size_t>::max();
    if (dist > desert_size)
      reset_points.push_back(i);
    prev_cpg = cpgs[i].get_start();
  }
  reset_points.push_back(cpgs.size());
  if (VERBOSE)
    cerr << "CPGS RETAINED: " << cpgs.size() << endl
         << "DESERTS REMOVED: " << reset_points.size() - 2 << endl << endl;
}


/*
 * FUNCTION TO "FOLD" THE METHYLATION PROFILE SO THAT THE MIDDLE
 * METHYLATION BECOMES LOWER METHYLATION, AND BOTH THE LOW AND HIGH
 * METHYLATION BECOME HIGH. THIS METHOD ACTUALLY SEEMS TO WORK.
 */
static void
make_partial_meth(vector<GenomicRegion> &cpgs) {
  for (size_t i = 0; i < cpgs.size(); ++i) {
    double cpg_meth = cpgs[i].get_score();
    if (cpg_meth > 0.5)
      cpg_meth = 1.0 - cpg_meth;
    cpgs[i].set_score(1.0 - (2*cpg_meth));
  }
}


static void
load_cpgs(const bool VERBOSE, const bool PARTIAL_METH,
          string cpgs_file, vector<SimpleGenomicRegion> &cpgs,
          vector<pair<double, double> > &meth, vector<size_t> &reads) {
  if (VERBOSE)
    cerr << "[READING CPGS AND METH PROPS]" << endl;
  vector<GenomicRegion> cpgs_in;
  ReadBEDFile(cpgs_file, cpgs_in);
  if (!check_sorted(cpgs_in))
    throw SMITHLABException("CpGs not sorted in file \"" + cpgs_file + "\"");

  if (PARTIAL_METH)
    make_partial_meth(cpgs_in);
  
  for (size_t i = 0; i < cpgs_in.size(); ++i) {
    cpgs.push_back(SimpleGenomicRegion(cpgs_in[i]));
    meth.push_back(std::make_pair(cpgs_in[i].get_score(), 0.0));
    const string r(cpgs_in[i].get_name());
    reads.push_back(atoi(r.substr(r.find_first_of(":") + 1).c_str()));
    meth.back().first = int(meth.back().first * reads.back());
    meth.back().second = int(reads.back() - meth.back().first);
  }
  if (VERBOSE)
    cerr << "TOTAL CPGS: " << cpgs.size() << endl
         << "MEAN COVERAGE: " 
         << accumulate(reads.begin(), reads.end(), 0.0)/reads.size() 
         << endl << endl;
}



static void
shuffle_cpgs(const TwoStateHMMB &hmm,
             vector<pair<double, double> > meth, 
             vector<size_t> reset_points, 
             const vector<double> &start_trans,
             const vector<vector<double> > &trans,
             const vector<double> &end_trans,
             const double fg_alpha, const double fg_beta, 
             const double bg_alpha, const double bg_beta,
             vector<double> &domain_scores) {
  srand(time(0) + getpid());
  random_shuffle(meth.begin(), meth.end());
  vector<bool> classes;
  vector<double> scores;
  hmm.PosteriorDecoding(meth, reset_points, start_trans, trans, 
                        end_trans, fg_alpha, fg_beta, bg_alpha, 
                        bg_beta, classes, scores);
  get_domain_scores(classes, meth, reset_points, domain_scores);
  sort(domain_scores.begin(), domain_scores.end());
}


static void
assign_p_values(const vector<double> &random_scores, 
                const vector<double> &observed_scores, 
                vector<double> &p_values) {
  const double n_randoms =
      random_scores.size() == 0 ? 1 : random_scores.size();
  for (size_t i = 0; i < observed_scores.size(); ++i)
    p_values.push_back((random_scores.end() - 
                        upper_bound(random_scores.begin(),
                                    random_scores.end(),
                                    observed_scores[i]))/n_randoms);
}

static void
read_params_file(const bool VERBOSE,
                 const string &params_file, 
                 double &fg_alpha, 
                 double &fg_beta, 
                 double &bg_alpha, 
                 double &bg_beta,
                 vector<double> &start_trans, 
                 vector<vector<double> > &trans, 
                 vector<double> &end_trans,
                 double &fdr_cutoff) {
  string jnk;
  std::ifstream in(params_file.c_str());
  in >> jnk >> fg_alpha
     >> jnk >> fg_beta 
     >> jnk >> bg_alpha
     >> jnk >> bg_beta
     >> jnk >> start_trans[0]
     >> jnk >> start_trans[1]
     >> jnk >> trans[0][0]
     >> jnk >> trans[0][1]
     >> jnk >> trans[1][0]
     >> jnk >> trans[1][1]
     >> jnk >> end_trans[0]
     >> jnk >> end_trans[1]
     >> jnk >> fdr_cutoff;
  if (VERBOSE)
    cerr << "FG_ALPHA\t" << fg_alpha << endl
         << "FG_BETA\t" << fg_beta << endl
         << "BG_ALPHA\t" << bg_alpha << endl
         << "BG_BETA\t" << bg_beta << endl
         << "S_F\t" << start_trans[0] << endl
         << "S_B\t" << start_trans[1] << endl
         << "F_F\t" << trans[0][0] << endl
         << "F_B\t" << trans[0][1] << endl
         << "B_F\t" << trans[1][0] << endl
         << "B_B\t" << trans[1][1] << endl
         << "F_E\t" << end_trans[0] << endl
         << "B_E\t" << end_trans[1] << endl
         << "FDR_CUTOFF\t" << fdr_cutoff << endl;
}

static void
write_params_file(const string &outfile, 
                  const double fg_alpha, 
                  const double fg_beta, 
                  const double bg_alpha, 
                  const double bg_beta,
                  const vector<double> &start_trans, 
                  const vector<vector<double> > &trans, 
                  const vector<double> &end_trans) {

  std::ofstream of;
  if (!outfile.empty()) of.open(outfile.c_str());
  std::ostream out(outfile.empty() ? std::cout.rdbuf() : of.rdbuf());
  
  out.precision(30);
  out << "FG_ALPHA\t" << fg_alpha << endl
      << "FG_BETA\t" << fg_beta << endl
      << "BG_ALPHA\t" << bg_alpha << endl
      << "BG_BETA\t" << bg_beta << endl
      << "S_F\t" << start_trans[0] << endl
      << "S_B\t" << start_trans[1] << endl
      << "F_F\t" << trans[0][0] << endl
      << "F_B\t" << trans[0][1] << endl
      << "B_F\t" << trans[1][0] << endl
      << "B_B\t" << trans[1][1] << endl
      << "F_E\t" << end_trans[0] << endl
      << "B_E\t" << end_trans[1] << endl
    ;
}


int
main(int argc, const char **argv) {

  try {

    string outfile;
    
    size_t desert_size = 1000;
    size_t max_iterations = 10;
    
    // run mode flags
    bool VERBOSE = false;
    bool PARTIAL_METH = false;
    
    // corrections for small values (not parameters):
    double tolerance = 1e-10;
    double min_prob  = 1e-10;

    string params_in_file;
    string params_out_file;
    
    /****************** COMMAND LINE OPTIONS ********************/
    OptionParser opt_parse(strip_path(argv[0]), "Program for identifying "
                           "HMRs in methylation data", "<cpg-BED-file>");
    opt_parse.add_opt("out", 'o', "output file (default: stdout)", 
                      false, outfile);
    opt_parse.add_opt("desert", 'd', "max dist btwn cpgs with reads in HMR", 
                      false, desert_size);
    opt_parse.add_opt("itr", 'i', "max iterations", false, max_iterations); 
    opt_parse.add_opt("verbose", 'v', "print more run info", false, VERBOSE);
    opt_parse.add_opt("partial", '\0', "identify PMRs instead of HMRs", 
                      false, PARTIAL_METH);
    opt_parse.add_opt("params-in", 'P', "HMM parameters file (no training)", 
                      false, params_in_file);
    opt_parse.add_opt("params-out", 'p', "write HMM parameters to this file", 
                      false, params_out_file);
    
    vector<string> leftover_args;
    opt_parse.parse(argc, argv, leftover_args);
    if (argc == 1 || opt_parse.help_requested()) {
      cerr << opt_parse.help_message() << endl
           << opt_parse.about_message() << endl;
      return EXIT_SUCCESS;
    }
    if (opt_parse.about_requested()) {
      cerr << opt_parse.about_message() << endl;
      return EXIT_SUCCESS;
    }
    if (opt_parse.option_missing()) {
      cerr << opt_parse.option_missing_message() << endl;
      return EXIT_SUCCESS;
    }
    if (leftover_args.empty()) {
      cerr << opt_parse.help_message() << endl;
      return EXIT_SUCCESS;
    }
    const string cpgs_file = leftover_args.front();
    /****************** END COMMAND LINE OPTIONS *****************/
    
    // separate the regions by chrom and by desert
    vector<SimpleGenomicRegion> cpgs;
    // vector<double> meth;
    vector<pair<double, double> > meth;
    vector<size_t> reads;
    load_cpgs(VERBOSE, PARTIAL_METH, cpgs_file, cpgs, meth, reads);
    
    // separate the regions by chrom and by desert, and eliminate
    // those isolated CpGs
    vector<size_t> reset_points;
    separate_regions(VERBOSE, desert_size, cpgs, meth, reads, reset_points);
    
    vector<double> start_trans(2, 0.5), end_trans(2, 1e-10);
    vector<vector<double> > trans(2, vector<double>(2, 0.25));
    trans[0][0] = trans[1][1] = 0.75;
    
    const TwoStateHMMB hmm(min_prob, tolerance, max_iterations, VERBOSE);
    
    double fg_alpha = 0;
    double fg_beta = 0;
    double bg_alpha = 0;
    double bg_beta = 0;
    
    double fdr_cutoff = std::numeric_limits<double>::max();

    if (!params_in_file.empty()) {
      // READ THE PARAMETERS FILE
      read_params_file(VERBOSE, params_in_file, 
                       fg_alpha, fg_beta, bg_alpha, bg_beta,
                       start_trans, trans, end_trans, fdr_cutoff);
    }
    else {
      const double n_reads = 
        accumulate(reads.begin(), reads.end(), 0.0)/reads.size();
      fg_alpha = 0.33*n_reads;
      fg_beta = 0.67*n_reads;
      bg_alpha = 0.67*n_reads;
      bg_beta = 0.33*n_reads;
    }
    
    if (max_iterations > 0)
      hmm.BaumWelchTraining(meth, reset_points, start_trans, trans, 
                            end_trans, fg_alpha, fg_beta, bg_alpha, bg_beta);
    
    if (!params_out_file.empty()) {
      // WRITE ALL THE HMM PARAMETERS:
      write_params_file(params_out_file, fg_alpha, fg_beta, bg_alpha, bg_beta,
                        start_trans, trans, end_trans);
    }
    
    /***********************************
     * STEP 5: DECODE THE DOMAINS
     */
    vector<bool> classes;
    vector<double> scores;
    hmm.PosteriorDecoding(meth, reset_points, start_trans, trans, 
                          end_trans, fg_alpha, fg_beta, bg_alpha, 
                          bg_beta, classes, scores);
    
    vector<double> domain_scores;
    get_domain_scores(classes, meth, reset_points, domain_scores);
    
    vector<double> random_scores;
    shuffle_cpgs(hmm, meth, reset_points, start_trans, trans, end_trans,
                 fg_alpha, fg_beta, bg_alpha, bg_beta, random_scores);
    
    vector<double> p_values;
    assign_p_values(random_scores, domain_scores, p_values);
    
    if (fdr_cutoff == numeric_limits<double>::max())
      fdr_cutoff = get_fdr_cutoff(p_values, 0.01);

    if (!params_out_file.empty()) {
      std::ofstream out(params_out_file.c_str(), std::ios::app);
      out << "FDR_CUTOFF\t" 
          << std::setprecision(30) << fdr_cutoff << endl;
      out.close();
    }
    
    vector<GenomicRegion> domains;
    build_domains(VERBOSE, cpgs, scores, reset_points, classes, domains);
    
    std::ofstream of;
    if (!outfile.empty()) of.open(outfile.c_str());
    std::ostream out(outfile.empty() ? std::cout.rdbuf() : of.rdbuf());
    
    size_t good_hmr_count = 0;
    for (size_t i = 0; i < domains.size(); ++i)
      if (p_values[i] < fdr_cutoff) {
        domains[i].set_name("HYPO" + smithlab::toa(good_hmr_count++));
        out << domains[i] << '\n';
      }
  }
  catch (SMITHLABException &e) {
    cerr << "ERROR:\t" << e.what() << endl;
    return EXIT_FAILURE;
  }
  catch (std::bad_alloc &ba) {
    cerr << "ERROR: could not allocate memory" << endl;
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
 
