use strict;
use warnings;
use SOAP::Lite;
use HTTP::Cookies;

sub convert_OFFICIAL_GENE_SYMBOL_to_ENSEMBL_GENE_ID ##since the David web service stopped support for OFFICIAL_GENE_SYMBOL
{
	my ($inputIds) = @_;
	my @outputIds = ();
	my @ids = split(/\,/, $inputIds);
	my %ens = ();
	open(IN, "./ensemblGene.v3.geneSymbolToId") or die;
	while(<IN>){
		chomp;
		my @f = split(/\t/, $_);
		$ens{$f[0]} = $f[1];
	}
	close(IN);
	foreach my $id (@ids){
		if(defined $ens{$id}){push(@outputIds, $ens{$id});}
	}
	return join(",", @outputIds);
}
sub convert_ENSEMBL_GENE_ID_to_OFFICIAL_GENE_SYMBOL 
{
	my ($inputIds) = @_;
	my @outputIds = ();
	$inputIds =~ s/ //g;
	my @ids = split(/\,/, $inputIds);
	my %ens = ();
	open(IN, "./ensemblGene.v3.geneSymbolToId") or die;
	while(<IN>){
		chomp;
		my @f = split(/\t/, $_);
		$ens{$f[1]} = $f[0];
	}
	close(IN);
	foreach my $id (@ids){
		if(defined $ens{$id}){push(@outputIds, $ens{$id});}
	}
	return join(",", @outputIds);
}


sub davidChartReport##($inputIds, $idType, $listName, $listType, $outfile)
{
	my ($inputIds, $idType, $listName, $listType, $outfile) = @_;
	my $soap = SOAP::Lite                             
	   -> uri('http://service.session.sample')                
	   -> proxy('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService',
		      cookie_jar => HTTP::Cookies->new(ignore_discard=>1));

	
	#user authentication by email address
	#For new user registration, go to http://david.abcc.ncifcrf.gov/knowledgebase/register.htm
	my $check = $soap->authenticate('yyin@ibt.tamhsc.edu')->result;
	      print "\nUser authentication: $check\n";
	
	if (lc($check) eq "true") { 
	
	
	
	#list conversion types
	my $conversionTypes = $soap ->getConversionTypes()->result;
	       print  "\nConversion Types: \n$conversionTypes\n"; 
	       
	#list all annotation category names
	my $allCategoryNames= $soap ->getAllAnnotationCategoryNames()->result;	 	  	
		print  "\nAll available annotation category names: \n$allCategoryNames\n"; 

 
	#addList
	#my $inputIds = '1000_at,1001_at,1002_f_at,1003_s_at,1004_at,1005_at,1006_at,1007_s_at,1008_f_at,1009_at,100_g_at,1010_at,1011_s_at,1012_at,1013_at,1014_at,1015_s_at,1016_s_at,1017_at,1018_at,1019_g_at,101_at,1020_s_at,1021_at,1022_f_at,1023_at,1024_at,1025_g_at,1026_s_at,1027_at,1028_at,1029_s_at,102_at,1030_s_at,1031_at,1032_at,1033_g_at,1034_at,1035_g_at,1036_at,1037_at,1038_s_at,1039_s_at,103_at,1040_s_at,1041_at,1042_at,1043_s_at,1044_s_at,1045_s_at,1046_at,1047_s_at,1048_at,1049_g_at,104_at,1050_at,1051_g_at,1052_s_at,1053_at,1054_at,1055_g_at,1056_s_at,1057_at,1058_at,1059_at,105_at,1060_g_at,1061_at,1062_g_at,1063_s_at,1064_at,1065_at,1066_at,1067_at,1068_g_at,1069_at,106_at,1070_at,1071_at,1072_g_at,1073_at,1074_at,1075_f_at,1076_at,1077_at,1078_at,1079_g_at,107_at,1080_s_at,1081_at,1082_at,1083_s_at,1084_at,1085_s_at,1086_at,1087_at,1088_at,1089_i_at,108_g_at,1090_f_at,1091_at,1092_at,1093_at,1094_g_at,1095_s_at,1096_g_at,1097_s_at,1098_at,1099_s_at,109_at,1100_at,1101_at,1102_s_at,1103_at,1104_s_at,1105_s_at,1106_s_at,1107_s_at,1108_s_at,1109_s_at,110_at,1110_at,1111_at,1112_g_at,1113_at,1114_at,1115_at,1116_at,1117_at,1118_at,1119_at,111_at,1120_at,1121_g_at,1122_f_at,1123_at,1124_at,1125_s_at,1126_s_at,1127_at,1128_s_at,1129_at,112_g_at,1130_at,1131_at,1132_s_at,1133_at,1134_at,1135_at,1136_at,1137_at,1138_at,1139_at,113_i_at,1140_at,1141_at,1142_at,1143_s_at,1144_at,1145_g_at,1146_at,1147_at,1148_s_at,1149_at,114_r_at,1150_at,1151_at,1152_i_at,1153_f_at,1154_at,1155_at,1156_at,1157_s_at,1158_s_at,1159_at,115_at,1160_at,1161_at,1162_g_at,1163_at,1164_at,1165_at,1166_at,1167_s_at,1168_at,1169_at,116_at,1170_at,1171_s_at,1172_at,1173_g_at,1174_at,1175_s_at,1176_at,1177_at,1178_at,1179_at,117_at,1180_g_at,1181_at,1182_at,1183_at,1184_at,1185_at,1186_at,1187_at,1188_g_at,1189_at,118_at,1190_at,1191_s_at,1192_at,1193_at,1194_g_at,1195_s_at,1196_at,1197_at,1198_at,1199_at,1200_at,1201_at,1202_g_at,1203_at,1204_at,1205_at,1206_at,1207_at,1208_at,1209_at,120_at,1210_s_at,1211_s_at,1212_at,1213_at,1214_s_at,1217_g_at,1218_at,1219_at,121_at,1220_g_at,1221_at,1222_at,1223_at,1224_at,1225_g_at,1226_at,1227_g_at,1228_s_at,1229_at,122_at,1230_g_at,1231_at,1232_s_at,1233_s_at,1234_at,1235_at,1236_s_at,1237_at,1238_at,1239_s_at,123_at,1240_at,1241_at,1242_at,1243_at,1244_at,1245_i_at,1246_at,1247_g_at,1248_at,1249_at,1250_at,1251_g_at,1252_at,1253_at,1254_at,1255_g_at,1256_at,1257_s_at,1258_s_at,1259_at,1260_s_at,1261_i_at,1262_s_at,1263_at,1264_at,1265_g_at,1266_s_at,1267_at,1268_at,1269_at,126_s_at,1270_at,1271_g_at,1272_at,1273_r_at,1274_s_at,1275_at,1276_g_at,1277_at,1278_at,1279_s_at,1280_i_at,1281_f_at,1282_s_at,1283_at,1284_at,1285_at,1286_s_at,1287_at,1288_s_at,1289_at,128_at,1290_g_at,1291_s_at,1292_at,1293_s_at,1294_at,1295_at,1296_at,1297_at,1298_at,1299_at,129_g_at,1300_at,1303_at,1304_at,1305_s_at,1306_at,1307_at,1308_g_at,1309_at,130_s_at,1310_at,1311_at,1312_at,1313_at,1314_at,1315_at,1316_at,1317_at,1318_at,1319_at,131_at,1320_at,1321_s_at,1322_at,1323_at,1324_at,1325_at,1326_at,1327_s_at,1328_at,1329_s_at,1330_at,1331_s_at,1332_f_at,1333_f_at,1334_s_at,1335_at,1336_s_at,1337_s_at,1338_s_at,1339_s_at,133_at,1340_s_at,1341_at,1342_g_at,1343_s_at,1344_at,1345_s_at,1346_at,1347_at,1348_s_at,1349_at,134_at,1350_at,1351_at,1352_at,1353_g_at,1354_at,1355_g_at,1356_at,1357_at,1358_s_at,1359_at,135_g_at,1360_at,1361_at,1362_s_at,1363_at,1364_at,1365_at,1366_i_at,1367_f_at,1368_at,1369_s_at,136_at,1370_at,1371_s_at,1372_at,1373_at,1374_g_at,1375_s_at,1376_at,1377_at,1378_g_at,1379_at,137_at,1380_at,1381_at,1382_at,1383_at,1384_at,1385_at,1386_at,1387_at,1388_g_at,1389_at,138_at,1390_s_at,1391_s_at,1392_at,1393_at,1394_at,1395_at,1396_at,1397_at,1398_g_at,1399_at,139_at,1400_at,1401_g_at,1402_at,1403_s_at,1404_r_at,1405_i_at,1406_at,1407_g_at,1408_at,1409_at,140_s_at,1410_at,1411_at,1412_g_at,1413_at,1414_at,1415_at,1416_g_at,1417_at,1418_at,1419_g_at,141_s_at,1420_s_at,1421_at,1422_g_at,1423_at,1424_s_at,1425_at,1426_at,1427_g_at,1428_at,142_at,1430_at,1431_at,1432_s_at,1433_g_at,1434_at,1435_f_at,1436_at,1437_at,1438_at,1439_s_at,143_s_at,1440_s_at,1441_s_at,1442_at,1443_at,1444_at,1445_at,1446_at,1447_at,1448_at,1449_at,144_at,1450_g_at,1451_s_at,1452_at,1453_at,1454_at,1455_f_at,1456_s_at,1457_at,1458_at,1459_at,145_s_at,1460_g_at,1461_at,1462_s_at,1463_at,1464_at,1465_s_at,1466_s_at,1467_at,1468_at,1469_at,146_at,1470_at,1471_at,1472_g_at,1473_s_at,1474_s_at,1475_s_at,1476_s_at,1477_s_at,1478_at,1479_g_at,147_at,1480_at,1481_at,1482_g_at,1483_at,1484_at,1485_at,1486_at,1487_at,1488_at,1489_s_at,148_at,1490_at,1491_at,1492_f_at,1493_r_at,1494_f_at,1495_at,1496_at,1497_at,1498_at,1499_at,149_at,1500_at,1501_at,1503_at,1504_s_at,1505_at,1506_at,1507_s_at,1508_at,1509_at,150_at,1510_g_at,1511_at,1512_at,1513_at,1514_g_at,1515_at,1516_g_at,1517_at,1518_at,1519_at,151_s_at,1520_s_at,1521_at,1522_at,1523_g_at,1524_at,1525_s_at,1526_i_at,1527_s_at,1528_at,1529_at,152_f_at,1530_g_at,1531_at,1532_g_at,1533_at,1534_at,1535_at,1536_at,1537_at,1538_s_at,1539_at,153_f_at,1540_f_at,1541_f_at,1542_at,1543_at,1544_at,1545_g_at,1546_at,1547_at,1548_s_at,1549_s_at,154_at,1550_at,1551_g_at,1552_i_at,1553_r_at,1554_f_at,1555_f_at,1556_at,1557_at,1558_g_at,1559_at,155_s_at,1560_g_at,1561_at,1562_g_at,1563_s_at,1564_at,1565_s_at,1566_at,1567_at,1568_s_at,1569_r_at,156_s_at,1570_f_at,1571_f_at,1572_s_at,1573_at,1574_s_at,1575_at,1576_g_at,1577_at,1578_g_at,1579_at,157_at,1580_f_at,1581_s_at,1582_at,1583_at,1584_at,1585_at,1586_at,1587_at,1588_at,1589_s_at,158_at,1590_s_at,1591_s_at,1592_at,1593_at,1594_at,1595_at,1596_g_at,1597_at,1598_g_at,1599_at,159_at,160020_at,160021_r_at,160022_at,160023_at,160024_at,160025_at,160026_at,160027_s_at,160028_s_at,160029_at,160030_at,160031_at,160032_at,160033_s_at,160034_s_at,160035_at,160036_at,160037_at,160038_s_at,160039_at,160040_at,160041_at,160042_s_at,160043_at,160044_g_at,1600_at,1601_s_at,1602_at,1603_g_at,1604_at,1605_g_at,1606_at,1607_at,1608_at,1609_g_at,160_at,1610_s_at,1611_s_at,1612_s_at,1613_s_at,1614_s_at,1615_at,1616_at,1617_at,1618_at,1619_g_at,161_at,1620_at,1621_at,1622_at,1623_s_at,1624_at,1625_at,1626_at,1627_at,1628_at,1629_s_at,162_at,1630_s_at,1631_at,1632_at,1633_g_at,1634_s_at,1635_at,1636_g_at,1637_at,1638_at,1639_s_at,163_at,1640_at,1641_s_at,1642_at,1643_g_at,1644_at,1645_at,1646_at,1647_at,1648_at,1649_at,164_at,1650_g_at,1651_at,1652_at,1653_at,1654_at,1655_s_at,1656_s_at,1657_at,1658_g_at,1659_s_at,165_g_at,1660_at,1661_i_at,1662_r_at,1663_at,1664_at,1665_s_at,1666_at,1667_s_at,1668_s_at,1669_at,166_at,1670_at,1671_s_at,1672_f_at,1673_at,1674_at,1675_at,1676_s_at,1677_at,1678_g_at,1679_at,167_at,1680_at,1681_at,1682_s_at,1683_at,1684_s_at,1685_at,1686_g_at,1687_s_at,1688_s_at,1689_at,168_at,1690_at,1691_at,1692_s_at,1693_s_at,1694_s_at,1695_at,1696_at,1697_s_at,1698_g_at,1699_at,169_at,1700_at,1701_at,1702_at,1703_g_at,1704_at,1705_s_at,1706_at,1707_g_at,1708_at,1709_g_at,170_at,1710_s_at,1711_at,1712_s_at,1713_s_at,1714_at,1715_at,1716_at,1717_s_at,1718_at,1719_at,171_at,1720_at,1721_g_at,1722_at,1723_g_at,1724_at,1725_s_at,1726_at,1727_at,1728_at,1729_at,172_at,1730_s_at,1731_at,1732_at,1733_at,1734_at,1735_g_at,1736_at,1737_s_at,1738_at,1739_at,173_at,1740_g_at,1741_s_at,1742_at,1743_s_at,1744_at,1745_at,1746_s_at,1747_at,1748_s_at,1749_at,174_s_at,1750_at,1751_g_at,1752_at,1753_s_at,1754_at,1755_i_at,1756_f_at,1757_i_at,1758_r_at,1759_f_at,175_s_at,1760_s_at,1761_at,1762_at,1763_at,1764_s_at,1765_at,1766_g_at,1767_s_at,1768_s_at,1769_at,176_at,1770_at,1771_s_at,1772_s_at,1773_at,1774_at,1775_at,1776_at,1777_at,1778_g_at,1779_s_at,177_at,1780_at,1781_at,1782_s_at,1783_at,1784_s_at,1785_at,1786_at,1787_at,1788_s_at,1789_at,178_f_at,1790_s_at,1791_s_at,1792_g_at,1793_at,1794_at,1795_g_at,1796_s_at,1797_at,1798_at,1799_at,179_at,1800_g_at,1801_at,1802_s_at,1803_at,1804_at,1805_g_at,1806_at,1807_g_at,1808_s_at,1809_at,180_at,1810_s_at,1811_at,1812_s_at,1813_at,1814_at,1815_g_at,1816_at,1817_at,1818_at,1819_at,181_g_at,1820_g_at,1821_at,1822_at,1823_g_at,1824_s_at,1825_at,1826_at,1827_s_at,1828_s_at,182_at,1830_s_at,1831_at,1832_at,1833_at,1834_at,1836_at,1837_at,1838_g_at,1839_at,183_at,1840_g_at,1841_s_at,1842_at,1843_at,1844_s_at,1845_at,1846_at,1847_s_at,1848_at,1849_s_at,184_at,1850_at,1851_s_at,1852_at,1853_at,1854_at,1855_at,1856_at,1857_at,1858_at,1859_s_at,185_at,1860_at,1861_at,1862_at,1863_s_at,1865_at,1866_g_at,1867_at,1868_g_at,1869_at,186_at,1870_at,1871_g_at,1872_at,1873_at,1874_at,1875_f_at,1876_at,1877_g_at,1878_g_at,1879_at,187_at,1880_at,1881_at,1882_g_at,1883_s_at,1884_s_at,1885_at,1886_at,1887_g_at,1888_s_at,188_at,1890_at,1891_at,1892_s_at,1893_s_at,1894_f_at,1895_at,1896_s_at,1897_at,1898_at,1899_s_at,189_s_at,1900_at,1901_s_at,1902_at,1903_at,1904_at,1905_s_at,1906_at,1907_at,1908_at,1909_at,190_at,1910_s_at,1911_s_at,1912_s_at,1913_at,1914_at,1915_s_at,1916_s_at,1917_at,1918_at,1919_at,191_at,1920_s_at,1921_at,1922_g_at,1923_at,1924_at,1925_at,1926_at,1927_s_at,1928_s_at,1929_at,192_at,1930_at,1931_at,1932_at,1933_g_at,1934_s_at,1935_at,1936_s_at,1937_at,1938_at,1939_at,193_at,1940_at,1941_at,1942_s_at,1943_at,1944_f_at,1945_at,1946_at,1947_g_at,1948_f_at,1949_at,194_at,1950_s_at,1951_at,1952_s_at,1953_at,1954_at,1955_s_at,1956_s_at,1957_s_at,1958_at,1959_at,195_s_at,1960_at,1961_f_at,1962_at,1963_at,1964_g_at,1965_s_at,1966_i_at,1967_f_at,1968_g_at,1969_s_at,196_s_at,1970_s_at,1971_g_at,1972_s_at,1973_s_at,1974_s_at,1975_s_at,1976_s_at,1977_s_at,1978_at,1979_s_at,197_at,1980_s_at,1981_s_at,1983_at,1984_s_at,1985_s_at,1986_at,1987_at,1988_at,1989_at,198_g_at,1990_g_at,1991_s_at,1992_at,1993_s_at,1994_at,1995_at,1996_s_at,1997_s_at,1998_i_at,1999_s_at,199_s_at,2000_at,2001_g_at,2002_s_at,2003_s_at,2004_at,2005_s_at,2006_at,2007_g_at,2008_s_at,2009_at,200_at,2010_at,2011_s_at,2012_s_at,2013_at,2014_s_at,2015_s_at,2016_s_at,2017_s_at,2018_at,2019_s_at,201_s_at,2020_at,2021_s_at,2022_at,2023_g_at,2024_s_at,2025_s_at,2026_at,2027_at,2028_s_at,2029_at,202_at,2030_at,2031_s_at,2032_s_at,2033_s_at,2034_s_at,2035_s_at,2036_s_at,2037_s_at,2038_g_at,2039_s_at,203_at,2040_s_at,2041_i_at,2042_s_at,2043_s_at,2044_s_at,2045_s_at,2046_at,2047_s_at,2048_s_at,2049_s_at,204_at,2050_s_at,2051_at,2052_g_at,2053_at,2054_g_at,2055_s_at,2056_at,2057_g_at,2058_s_at,2059_s_at,205_g_at,2060_at,2061_at,2062_at,2063_at,2064_g_at,2065_s_at,2066_at,2067_f_at,2068_s_at,2069_s_at,206_at,2070_i_at,2071_s_at,2072_at,2073_s_at,2074_at,2075_s_at,2076_s_at,2077_at,2078_s_at,2079_s_at,207_at,2080_s_at,2081_s_at,2082_s_at,2083_at,2084_s_at,2085_s_at,2086_s_at,2087_s_at,2088_s_at,2089_s_at,208_at,2090_i_at,2091_at,2092_s_at,2093_s_at,2094_s_at,209_at,210_at,211_at,212_at,213_at,214_at,215_g_at,216_at,217_at,218_at,219_i_at,220_r_at,221_s_at,222_at,223_at,224_at,225_at,226_at,227_g_at,228_at,229_at,230_s_at,231_at,232_at,233_s_at,234_s_at,235_at,236_at,237_s_at,238_at,239_at,240_at,241_g_at,242_at,243_g_at,244_at,245_at,246_at,247_s_at,248_at,249_at,250_at,251_at,252_at,253_g_at,254_at,255_s_at,256_s_at,257_at,258_at,259_s_at,260_at,261_s_at,262_at,263_g_at,264_at,265_s_at,266_s_at,267_at,268_at,269_at,270_at,271_s_at,272_at,273_g_at,274_at,275_at,276_at,277_at,278_at,279_at,280_g_at,281_s_at,282_at,283_at,284_at,285_g_at,286_at,287_at,288_s_at,289_at,290_s_at,291_s_at,292_s_at,293_at,294_s_at,295_s_at,296_at,297_g_at,298_at,299_i_at,300_f_at,301_at,302_at,303_at,304_at,305_g_at,306_s_at,307_at,308_f_at,309_f_at,310_s_at,311_s_at,312_s_at,31307_at,31308_at,31309_r_at,31310_at,31311_at,31312_at,31313_at,31314_at,31315_at,31316_at,31317_r_at,31318_at,31319_at,31320_at,31321_at,31322_at,31323_r_at,31324_at,31325_at,31326_at,31327_at,31328_at,31329_at,31330_at,31331_at,31332_at,31333_at,31334_at,31335_at,31336_at,31337_at,31338_at,31339_at,31340_at,31341_at,31342_at,31343_at,31344_at,31345_at,31346_at,31347_at,31348_at,31349_at,31350_at,31351_at,31352_at,31353_f_at,31354_r_at,31355_at,31356_at,31357_at,31358_at,31359_at,31360_at,31361_at,31362_at,31363_at,31364_i_at,31365_f_at,31366_at,31367_at,31368_at,31369_at,31370_at,31371_at,31372_at,31373_at,31374_at,31375_at,31376_at,31377_r_at,31378_at,31379_at,31380_at,31381_at,31382_f_at,31383_at,31384_at,31385_at,31386_at,31387_at,31388_at,31389_at,31390_at,31391_at,31392_r_at,31393_r_at,31394_at,31395_i_at,31396_r_at,31397_at,31398_at,31399_at,313_at,31400_at,31401_r_at,31402_at,31403_at,31404_at,31405_at,31406_at,31407_at,31408_at,31409_at,31410_at,31411_at,31412_at,31413_at,31414_at,31415_at,31416_at,31417_at,31418_at,31419_r_at,31420_at,31421_at,31422_at,31423_at,31424_at,31425_g_at,31426_at,31427_at,31428_at,31429_at,31430_at,31431_at,31432_g_at,31433_at,31434_at,31435_at,31436_s_at,31437_r_at,31438_s_at,31439_f_at,31440_at,31441_at,31442_at,31443_at,31444_s_at,31445_at,31446_s_at,31447_at,31448_s_at,31449_at,31450_s_at,31451_at,31452_at,31453_s_at,31454_f_at,31455_r_at,31456_at,31457_at,31458_at,31459_i_at,31460_f_at,31461_at,31462_f_at,31463_s_at,31464_at,31465_g_at,31466_at,31467_at,31468_f_at,31469_s_at,31470_at,31471_at,31472_s_at,31473_s_at,31474_r_at,31475_at,31476_g_at,31477_at,31478_at,31479_f_at,31480_f_at,31481_s_at,31482_at,31483_g_at,31484_at,31485_at,31486_s_at,31487_at,31488_s_at,31489_at,31490_at,31491_s_at,31492_at,31493_s_at,31494_at,31495_at,31496_g_at,31497_at,31498_f_at,31499_s_at,314_at,31500_at,31501_at,31502_at,31503_at,31504_at,31505_at,31506_s_at,31507_at,31508_at,31509_at,31510_s_at,31511_at,31512_at,31513_at,31514_at,31515_at,31516_f_at,31517_f_at,31518_i_at,31519_f_at,31520_at,31521_f_at,31522_f_at,31523_f_at,31524_f_at,31525_s_at,31526_f_at,31527_at,31528_f_at,31529_at,31530_at,31531_g_at,31532_at,31533_s_at,31534_at,31535_i_at,31536_at,31537_at,31538_at,31539_r_at,31540_at,31541_at,31542_at,31543_at,31544_at,31545_at,31546_at,31547_at,31548_at,31549_at,31550_at,31551_at,31552_at,31553_at,31554_at,31555_at,31556_at,31557_at,31558_at,31559_at,31560_at,31561_at,31562_at,31563_at,31564_at,31565_at,31566_at,31567_at,31568_at,31569_at,31570_at,31571_at,31572_at,31573_at,31574_i_at,31575_f_at,31576_at,31577_at,31578_at,31579_at,31580_at,31581_at,31582_at,31583_at,31584_at,31585_at,31586_f_at,31587_at,31588_at,31589_at,31590_g_at,31591_s_at,31592_at,31593_at,31594_at,31595_at,31596_f_at,31597_r_at,31598_s_at,31599_f_at,315_at,31600_s_at,31601_s_at,31602_at,31603_at,31604_at,31605_at,31606_at,31607_at,31608_g_at,31609_s_at,31610_at,31611_s_at,31612_at,31613_at,31614_at,31615_i_at,31616_r_at,31617_at,31618_at,31619_at,31620_at,31621_s_at,31622_f_at,31623_f_at,31624_at,31625_at,31626_i_at,31627_f_at,31628_at,31629_at,31630_at,31631_f_at,31632_at,31633_g_at,31634_at,31635_g_at,31636_s_at,31637_s_at,31638_at,31639_f_at,31640_r_at,31641_s_at,31642_at,31643_at,31644_at,31645_at,31646_at,31647_at,31648_at,31649_at,31650_g_at,31651_at,31652_at,31653_at,31654_at,31655_at,31656_at,31657_at,31658_at,31659_at,31660_at,31661_at,31662_at,31663_at,31664_at,31665_s_at,31666_f_at,31667_r_at,31668_f_at,31669_s_at,31670_s_at,31671_at,31672_g_at,31673_s_at,31674_s_at,31675_s_at,31676_at,31677_at,31678_at,31679_at,31680_at,31681_at,31682_s_at,31683_at,31684_at,31685_at,31686_at,31687_f_at,31688_at,31689_at,31690_at,31691_g_at,31692_at,31693_f_at,31694_at,31695_g_at,31696_at,31697_s_at,31698_at,31699_at,316_g_at,31700_at,31701_r_at,31702_at,31703_at,31704_at,31705_at,31706_at,31707_at,31708_at,31709_at,31710_at,31711_at,31712_at,31713_s_at,31714_at,31715_at,31716_at,31717_at,31718_at,31719_at,31720_s_at,31721_at,31722_at,31723_at,31724_at,31725_s_at,31726_at,31727_at,31728_at,31729_at,31730_at,31731_at,31732_at,31733_at,31734_at,31735_at,31736_at,31737_at,31738_at,31739_at,31740_s_at,31741_at,31742_at,31743_at,31744_at,31745_at,31746_at,31747_g_at,31748_at,31749_f_at,31750_at,31751_f_at,31752_at,31753_at,31754_at,31755_at,31756_at,31757_at,31758_at,31759_at,31760_at,31761_at,31762_at,31763_at,31764_at,31765_at,31766_s_at,31767_at,31768_at,31769_at,31770_at,31771_at,31772_at,31773_at,31774_at,31775_at,31776_at,31777_at,31778_at,31779_s_at,31780_f_at,31781_at,31782_at,31783_at,31784_at,31785_f_at,31786_at,31787_at,31788_at,31789_at,31790_at,31791_at,31792_at,31793_at,31794_at,31795_at,31796_at,31797_at,31798_at,31799_at,317_at,31800_at,31801_at,31802_at,31803_at,31804_f_at,31805_at,31806_at,31807_at,31808_at,31809_at,31810_g_at,31811_r_at,31812_at,31813_at,31814_i_at,31815_r_at,31816_at,31817_at,31818_at,31819_at,31820_at,31821_at,31822_at,31823_at,31824_at,31825_at,31826_at,31827_s_at,31828_r_at,31829_r_at,31830_s_at,31831_at,31832_at,31833_at,31834_r_at,31835_at,31836_at,31837_at,31838_at,31839_at,31840_at,31841_at,31842_at,31843_at,31844_at,31845_at,31846_at,31847_at,31848_at,31849_at,31850_at,31851_at,31852_at,31853_at,31854_at,31855_at,31856_at,31857_r_at,31858_at,31859_at,31860_at,31861_at,31862_at,31863_at,31864_at,31865_at,31866_at,31867_at,31868_at,31869_at,31870_at,31871_r_at,31872_at,31873_at,31874_at,31875_at,31876_r_at,31877_at,31878_at,31879_at,31880_at,31881_at,31882_at,31883_at,31884_at,31885_at,31886_at,31887_at,31888_s_at,31889_at,31890_s_at,31891_at,31892_at,31893_at,31894_at,31895_at,31896_at,31897_at,31898_at,31899_at,318_at,31900_at,31901_at,31902_at,31903_at,31904_at,31905_at,31906_at,31907_at,31908_at,31909_at,31910_at,31911_at,31912_at,31913_at,31914_at,31915_at,31916_at,31917_at,31918_at,31919_at,31920_at,31921_at,31922_i_at,31923_f_at,31924_at,31925_s_at,31926_at,31927_s_at,31928_at,31929_at,31930_f_at,31931_f_at,31932_f_at,31933_r_at,31934_at,31935_s_at,31936_s_at,31937_at,31938_g_at,31939_at,31940_s_at,31941_s_at,31942_at,31943_g_at,31944_at,31945_s_at,31946_s_at,31947_r_at,31948_at,31949_at,31950_at,31951_s_at,31952_at,31953_f_at,31954_f_at,31955_at,31956_f_at,31957_r_at,31958_i_at,31959_at,31960_f_at,31961_r_at,31962_at,31963_at,31964_at,31965_at,31966_at,31967_at,31968_at,31969_i_at,31970_r_at,31971_at,31972_at,31973_at,31974_at,31975_at,31976_at,31977_at,31978_at,31979_at,31980_at,31981_at,31982_at,31983_at,31984_at,31985_at,31986_at,31987_at,31988_at,31989_s_at,31990_at,31991_at,31992_f_at,31993_f_at,31994_at,31995_g_at,31996_at,31997_at,31998_at,31999_at,319_g_at,32000_g_at,32001_s_at,32002_at,32003_at,32004_s_at,32005_at,32006_r_at,32007_at,32008_at,32009_at,32010_at,32011_g_at,32012_at,32013_at,32014_at,32015_at,32016_at,32017_at,32018_at,32019_at,32020_at,32021_at,32022_at,32023_at,32024_at,32025_at,32026_s_at,32027_at,32028_at,32029_at,32030_at,32031_at,32032_at,32033_at,32034_at,32035_at,32036_i_at,32037_r_at,32038_s_at,32039_at,32040_i_at,32041_r_at,32042_at,32043_at,32044_at,32045_at,32046_at,32047_at,32048_at,32049_f_at,32050_r_at,32051_at,32052_at,32053_at,32054_at,32055_g_at,32056_at,32057_at,32058_at,32059_at,32060_at,32061_at,32062_at,32063_at,32064_at,32065_at,32066_g_at,32067_at,32068_at,32069_at,32070_at,32071_at,32072_at,32073_at,32074_at,32075_at,32076_at,32077_s_at,32078_at,32079_at,32080_at,32081_at,32082_at,32083_at,32084_at,32085_at,32086_at,32087_at,32088_at,32089_at,32090_at,32091_at,32092_at,32093_at,32094_at,32095_at,32096_at,32097_at,32098_at,32099_at,320_at,32100_r_at,32101_at,32102_at,32103_at,32104_i_at,32105_f_at,32106_at,32107_at,32108_at,32109_at,32110_at,32111_at,32112_s_at,32113_at,32114_s_at,32115_r_at,32116_at,32117_at,32118_at,32119_at,32120_at,32121_at,32122_at,32123_at,32124_at,32125_at,32126_at,32127_at,32128_at,32129_at,32130_at,32131_at,32132_at,32133_at,32134_at,32135_at,32136_r_at,32137_at,32138_at,32139_at,32140_at,32141_at,32142_at,32143_at,32144_at,32145_at,32146_s_at,32147_at,32148_at,32149_at,32150_at,32151_at,32152_at,32153_s_at,32154_at,32155_at,32156_at,32157_at,32158_at,32159_at,32160_at,32161_at,32162_r_at,32163_f_at,32164_at,32165_at,32166_at,32167_at,32168_s_at,32169_at,32170_g_at,32171_at,32172_at,32173_at,32174_at,32175_at,32176_at,32177_s_at,32178_r_at,32179_s_at,32180_s_at,32181_at,32182_at,32183_at,32184_at,32185_at,32186_at,32187_at,32188_at,32189_g_at,32190_at,32191_at,32192_g_at,32193_at,32194_at,32195_at,32196_at,32197_at,32198_at,32199_at,321_at,32200_at,32201_at,32202_at,32203_at,32204_at,32205_at,32206_at,32207_at,32208_at,32209_at,32210_at,32211_at,32212_at,32213_at,32214_at,32215_i_at,32216_r_at,32217_at,32218_at,32219_at,32220_at,32221_at,32222_at,32223_at,32224_at,32225_at,32226_at,32227_at,32228_at,32229_at,32230_at,32231_at,32232_at,32233_at,32234_at,32235_at,32236_at,32237_at,32238_at,32239_at,32240_at,32241_at,32242_at,32243_g_at,32244_at,32245_at,32246_g_at,32247_at,32248_at,32249_at,32250_at,32251_at,32252_at,32253_at,32254_at,32255_i_at,32256_r_at,32257_f_at,32258_r_at,32259_at,32260_at,32261_at,32262_at,32263_at,32264_at,32265_at,32266_at,32267_at,32268_at,32269_at,32270_g_at,32271_at,32272_at,32273_at,32274_r_at,32275_at,32276_at,32277_at,32278_at,32279_at,32280_at,32281_at,32282_at,32283_at,32284_at,32285_g_at,32286_at,32287_s_at,32288_r_at,32289_at,32290_at,32291_at,32292_at,32293_at,32294_g_at,32295_at,32296_at,32297_s_at,32298_at,32299_at,322_at,32300_s_at,32301_at,32302_g_at,32303_at,32304_at,32305_at,32306_g_at,32307_s_at,32308_r_at,32309_at,32310_f_at,32311_r_at,32312_at,32313_at,32314_g_at,32315_at,32316_s_at,32317_s_at,32318_s_at,32319_at,32320_at,32321_at,32322_at,32323_at,32324_at,32325_at,32326_at,32327_at,32328_at,32329_at,32330_at,32331_at,32332_at,32333_at,32334_f_at,32335_r_at,32336_at,32337_at,32338_at,32339_at,32340_s_at,32341_f_at,32342_at,32343_at,32344_r_at,32345_at,32346_at,32347_at,32348_at,32349_at,32350_at,32351_at,32352_at,32353_at,32354_at,32355_at,32356_at,32357_at,32358_at,32359_at,32360_s_at,32361_s_at,32362_r_at,32363_at,32364_at,32365_at,32366_at,32367_at,32368_at,32369_at,32370_at,32371_at,32372_at,32373_at,32374_at,32375_at,32376_at,32377_at,32378_at,32379_f_at,32380_at,32381_at,32382_at,32383_at,32384_g_at,32385_at,32386_at,32387_at,32388_at,32389_at,32390_at,32391_g_at,32392_s_at,32393_s_at,32394_s_at,32395_r_at,32396_f_at,32397_r_at,32398_s_at,32399_at,323_at,32400_at,32401_at,32402_s_at,32403_at,32404_at,32405_at,32406_at,32407_f_at,32408_s_at,32409_at,32410_at,32411_at,32412_at,32413_at,32414_at,32415_at,32416_at,32417_at,32418_at,32419_at,32420_at,32421_at,32422_at,32423_at,32424_at,32425_at,32426_f_at,32427_at,32428_at,32429_f_at,32430_at,32431_at,32432_f_at,32433_at,32434_at,32435_at,32436_at,32437_at,32438_at,32439_at,32440_at,32441_at,32442_at,32443_at,32444_at,32445_at,32446_at,32447_at,32448_at,32449_at,32450_at,32451_at,32452_at,32453_at,32454_at,32455_s_at,32456_s_at,32457_f_at,32458_f_at,32459_at,32460_at,32461_f_at,32462_s_at,32463_at,32464_at,32465_at,32466_at,32467_at,32468_f_at,32469_at,32470_at,32471_at,32472_at,32473_at,32474_at,32475_at,32476_at,32477_at,32478_f_at,32479_at,32480_at,32481_at,32482_at,32483_at,32484_at,32485_at,32486_at,32487_s_at,32488_at,32489_at,32490_at,32491_at,32492_g_at,32493_at,32494_at,32495_at,32496_at,32497_s_at,32498_at,32499_at,324_f_at,32500_at,32501_at,32502_at,32503_at,32504_at,32505_at,32506_at,32507_at,32508_at,32509_at,32510_at,32511_at,32512_at,32513_at,32514_s_at,32515_s_at,32516_at,32517_at,32518_at,32519_at,32520_at,32521_at,32522_f_at,32523_at,32524_s_at,32525_r_at,32526_at,32527_at,32528_at,32529_at,32530_at,32531_at,32532_at,32533_s_at,32534_f_at,32535_at,32536_at,32537_at,32538_at,32539_at,32540_at,32541_at,32542_at,32543_at,32544_s_at,32545_r_at,32546_at,32547_at,32548_at,32549_at,32550_r_at,32551_at,32552_at,32553_at,32554_s_at,32555_at,32556_at,32557_at,32558_at,32559_s_at,32560_s_at,32561_at,32562_at,32563_at,32564_at,32565_at,32566_at,32567_at,32568_at,32569_at,32570_at,32571_at,32572_at,32573_at,32574_at,32575_at,32576_at,32577_s_at,32578_at,32579_at,32580_at,32581_at,32582_at,32583_at,32584_at,32585_at,32586_at,32587_at,32588_s_at,32589_at,32590_at,32591_at,32592_at,32593_at,32594_at,32595_at,32596_at,32597_at,32598_at,32599_at,325_s_at,32600_at,32601_s_at,32602_at,32603_at,32604_s_at,32605_r_at,32606_at,32607_at,32608_at,32609_at,32610_at,32611_at,32612_at,32613_at,32614_at,32615_at,32616_at,32617_at,32618_at,32619_at,32620_at,32621_at,32622_at,32623_at,32624_at,32625_at,32626_at,32627_at,32628_at,32629_f_at,32630_f_at,32631_at,32632_g_at,32633_at,32634_s_at,32635_at,32636_f_at,32637_r_at,32638_s_at,32639_at,32640_at,32641_at,32642_at,32643_at,32644_at,32645_at,32646_at,32647_at,32648_at,32649_at,32650_at,32651_at,32652_g_at,32653_at,32654_g_at,32655_s_at,32656_at,32657_at,32658_at,32659_at,32660_at,32661_s_at,32662_at,32663_at,32664_at,32665_at,32666_at,32667_at,32668_at,32669_at,32670_at,32671_at,32672_at,32673_at,32674_at,32675_at,32676_at,32677_at,32678_at,32679_at,32680_at,32681_at,32682_at,32683_at,32684_at,32685_at,32686_at,32687_s_at,32688_at,32689_s_at,32690_s_at,32691_s_at,32692_at,32693_at,32694_at,32695_at,32696_at,32697_at,32698_at,32699_s_at,326_i_at,32700_at,32701_at,32702_at,32703_at,32704_at,32705_at,32706_at,32707_at,32708_g_at,32709_at,32710_at,32711_g_at,32712_at,32713_at,32714_s_at,32715_at,32716_at,32717_at,32718_at,32719_at,32720_at,32721_at,32722_at,32723_at,32724_at,32725_at,32726_g_at,32727_at,32728_at,32729_at,32730_at,32731_at,32732_at,32733_at,32734_at,32735_at,32736_at,32737_at,32738_at,32739_at,32740_at,32741_at,32742_s_at,32743_at,32744_at,32745_at,32746_at,32747_at,32748_at,32749_s_at,32750_r_at,32751_at,32752_at,32753_at,32754_at,32755_at,32756_at,32757_at,32758_g_at,32759_at,32760_at,32761_at,32762_i_at,32763_r_at,32764_at,32765_f_at,32766_at,32767_at,32768_at,32769_at,32770_at,32771_at,32772_s_at,32773_at,32774_at,32775_r_at,32776_at,32777_at,32778_at,32779_s_at,32780_at,32781_f_at,32782_r_at,32783_at,32784_at,32785_at,32786_at,32787_at,32788_at,32789_at,32790_at,32791_at,32792_at,32793_at,32794_g_at,32795_at,32796_f_at,32797_at,32798_at,32799_at,327_f_at,32800_at,32801_at,32802_at,32803_at,32804_at,32805_at,32806_at,32807_at,32808_at,32809_at,32810_at,32811_at,32812_at,32813_s_at,32814_at,32815_at,32816_at,32817_at,32818_at,32819_at,32820_at,32821_at,32822_at,32823_at,32824_at,32825_at,32826_at,32827_at,32828_at,32829_at,32830_g_at,32831_at,32832_at,32833_at,32834_r_at,32835_at,32836_at,32837_at,32838_at,32839_at,32840_at,32841_at,32842_at,32843_s_at,32844_at,32845_at,32846_s_at,32847_at,32848_at,32849_at,32850_at,32851_at,32852_at,32853_at,32854_at,32855_at,32856_at,32857_at,32858_at,32859_at,32860_g_at,32861_s_at,32862_at,32863_at,32864_at,32865_at,32866_at,32867_at,32868_at,32869_at,32870_g_at,32871_at,32872_at,32873_at,32874_at,32875_at,32876_s_at,32877_i_at,32878_f_at,32879_at,32880_at,32881_at,32882_at,32883_at,32884_at,32885_f_at,32886_at,32887_at,32888_at,32889_at,32890_at,32891_at,32892_at,32893_s_at,32894_at,32895_f_at,32896_at,32897_at,32898_at,32899_s_at,328_at,32900_at,32901_s_at,32902_at,32903_at,32904_at,32905_s_at,32906_at,32907_at,32908_at,32909_at,32910_at,32911_s_at,32912_at,32913_i_at,32914_f_at,32915_at,32916_at,32917_at,32918_at,32919_at,32920_at,32921_at,32922_at,32923_r_at,32924_at,32925_at,32926_at,32927_at,32928_at,32929_at,32930_f_at,32931_at,32932_at,32933_r_at,32934_i_at,32935_at,32936_at,32937_at,32938_at,32939_g_at,32940_at,32941_at,32942_at,32943_at,32944_at,32945_i_at,32946_r_at,32947_at,32948_at,32949_at,32950_at,32951_g_at,32952_at,32953_at,32954_at,32955_at,32956_at,32957_g_at,32958_at,32959_at,32960_at,32961_at,32962_at,32963_s_at,32964_at,32965_f_at,32966_at,32967_at,32968_s_at,32969_r_at,32970_f_at,32971_at,32972_at,32973_s_at';
	#my $idType = 'OFFICIAL_GENE_SYMBOL';
	#my $listName = 'make_up';
	#my $listType=0;
	#
	######since the David web service stopped support for OFFICIAL_GENE_SYMBOL
	my $old_idType = $idType;
	if($idType eq "OFFICIAL_GENE_SYMBOL"){$idType = "ENSEMBL_GENE_ID";}
	$inputIds = convert_OFFICIAL_GENE_SYMBOL_to_ENSEMBL_GENE_ID($inputIds);
	######since the David web service stopped support for OFFICIAL_GENE_SYMBOL
	
	print join("\n", $inputIds, $idType, $listName, $listType), "\n";
	
	my $list = $soap ->addList($inputIds, $idType, $listName, $listType)->result;
	print "\n$list of list was mapped\n"; 
	      
	#list all species  names
	my $allSpecies= $soap ->getSpecies()->result;	 	  	
	print  "\nAll species: \n$allSpecies\n"; 
	
	#list current species  names
	my $currentSpecies= $soap ->getCurrentSpecies()->result;	 	  	
	print  "\nCurrent species: \n$currentSpecies\n"; 
	
	#set user defined species 
	my $species = $soap ->setCurrentSpecies("0")->result;
	
	print "\nCurrent species: \n$species\n"; 
	#die;
	#set user defined categories 
	my $categories = $soap ->setCategories("abcd,BBID,BIOCARTA,COG_ONTOLOGY,GOTERM_BP_FAT,GOTERM_CC_FAT,GOTERM_MF_FAT,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,SP_PIR_KEYWORDS,UP_SEQ_FEATURE")->result;
	#to user DAVID default categories, send empty string to setCategories():
	#my $categories = $soap ->setCategories("")->result;
	#print "\nValid categories: \n$categories\n\n";  
	
	open (chartReport, ">", $outfile) or die;
	print chartReport "Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n";
	#close chartReport;
	
	#open (chartReport, ">>", "chartReport.txt");
	#getChartReport 	
	my $thd=0.1;
	my $ct = 2;
	my $chartReport = $soap->getChartReport($thd,$ct);
	      my @chartRecords = $chartReport->paramsout;
	      #shift(@chartRecords,($chartReport->result));
	      #print $chartReport->result."\n";
	      print "Total chart records: ".(@chartRecords)."\n";
	      print "\n ";
	      if( @chartRecords == 0 ){ return; }
	      #my $retval = %{$chartReport->result};
	      my @chartRecordKeys = keys %{$chartReport->result};
	      
	      #print "@chartRecordKeys\n";
	      
	      my @chartRecordValues = values %{$chartReport->result};
	      
	      my %chartRecord = %{$chartReport->result};
	      my $categoryName = $chartRecord{"categoryName"};
	      my $termName = $chartRecord{"termName"};
	      my $listHits = $chartRecord{"listHits"};
	      my $percent = $chartRecord{"percent"};
	      my $ease = $chartRecord{"ease"};
	      my $Genes = $chartRecord{"geneIds"};
	      my $listTotals = $chartRecord{"listTotals"};
	      my $popHits = $chartRecord{"popHits"};
	      my $popTotals = $chartRecord{"popTotals"};
	      my $foldEnrichment = $chartRecord{"foldEnrichment"};
	      my $bonferroni = $chartRecord{"bonferroni"};
	      my $benjamini = $chartRecord{"benjamini"};
	      my $FDR = $chartRecord{"afdr"};
	      
	      if($old_idType eq "OFFICIAL_GENE_SYMBOL"){ $Genes = convert_ENSEMBL_GENE_ID_to_OFFICIAL_GENE_SYMBOL($Genes);}
	      
	      print chartReport "$categoryName\t$termName\t$listHits\t$percent\t$ease\t$Genes\t$listTotals\t$popHits\t$popTotals\t$foldEnrichment\t$bonferroni\t$benjamini\t$FDR\n";
	      
	      
	      for my $j (0 .. (@chartRecords-1))
	      {			
		      %chartRecord = %{$chartRecords[$j]};
		      $categoryName = $chartRecord{"categoryName"};
		      $termName = $chartRecord{"termName"};
		      $listHits = $chartRecord{"listHits"};
		      $percent = $chartRecord{"percent"};
		      $ease = $chartRecord{"ease"};
		      $Genes = $chartRecord{"geneIds"};
		      $listTotals = $chartRecord{"listTotals"};
		      $popHits = $chartRecord{"popHits"};
		      $popTotals = $chartRecord{"popTotals"};
		      $foldEnrichment = $chartRecord{"foldEnrichment"};
		      $bonferroni = $chartRecord{"bonferroni"};
		      $benjamini = $chartRecord{"benjamini"};
		      $FDR = $chartRecord{"afdr"};			
		      
		      if($old_idType eq "OFFICIAL_GENE_SYMBOL"){ $Genes = convert_ENSEMBL_GENE_ID_to_OFFICIAL_GENE_SYMBOL($Genes);}
	      
		      print chartReport "$categoryName\t$termName\t$listHits\t$percent\t$ease\t$Genes\t$listTotals\t$popHits\t$popTotals\t$foldEnrichment\t$bonferroni\t$benjamini\t$FDR\n";				 
	      }		  	
	      
	      close chartReport;
	      print "\n$outfile generated\n";
	}
}
1;

=pod
#!perl
  #use strict;
  #use warnings;
  use SOAP::Lite;
  use HTTP::Cookies;

  my $soap = SOAP::Lite                             
     -> uri('http://service.session.sample')                
     -> proxy('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService',
                cookie_jar => HTTP::Cookies->new(ignore_discard=>1));

 #user authentication by email address
 #For new user registration, go to http://david.abcc.ncifcrf.gov/webservice/register.htm
 my $check = $soap->authenticate('deqiangs@bcm.edu')->result;
  	print "\nUser authentication: $check\n";

 if (lc($check) eq "true") { 


 
 #list conversion types
 my $conversionTypes = $soap ->getConversionTypes()->result;
	 print  "\nConversion Types: \n$conversionTypes\n"; 
	 
 #list all annotation category names
 my $allCategoryNames= $soap ->getAllAnnotationCategoryNames()->result;	 	  	
 print  "\nAll available annotation category names: \n$allCategoryNames\n"; 
 
 #addList
 my $inputIds = '31741_at,31734_at,32696_at,37559_at,41400_at,35985_at,39304_g_at,41438_at,35067_at,32919_at,35429_at,36674_at,967_g_at,36669_at,39242_at,39573_at,39407_at,33346_r_at,40319_at,2043_s_at,1788_s_at,36651_at,41788_i_at,35595_at,36285_at,39586_at,35160_at,39424_at,36865_at,2004_at,36728_at,37218_at,40347_at,36226_r_at,33012_at,37906_at,32872_at,989_at,32718_at,36957_at,32645_at,37628_at,33825_at,35687_at,32779_s_at,34493_at,31564_at,887_at,34712_at,32897_at,34294_at,41365_at,41446_f_at,34375_at,875_g_at,41099_at,919_at,38970_s_at,39159_at,34184_at,1018_at,38032_at,35956_s_at,35536_at,34562_at,1867_at,35957_at,39519_at,41657_at,38491_at,652_g_at,35776_at,34989_at,33455_at,39950_at,37723_at,31977_at,38629_at,34581_s_at,36210_g_at,35120_at,41532_at,37889_at,1332_f_at,40540_at,41105_s_at,1919_at,37542_at,39698_at,36711_at,36809_at,1167_s_at,31648_at,32364_at,40792_s_at,38685_at,41358_at,32931_at,35294_at,39870_at,38654_at,257_at,39071_at,35606_at,41726_at,33094_s_at,32405_at,1432_s_at,33698_at,408_at,39748_at,1953_at,36100_at,36101_s_at,1372_at,35314_at,40790_at,2030_at,179_at,1852_at,259_s_at,38024_at,35376_f_at,41779_at,39232_at,41159_at,40365_at,31626_i_at,40385_at,35613_at,37506_at,38207_at,887_at,600_at,1461_at,38691_s_at,1267_at,1177_at,1125_s_at,2036_s_at,31615_i_at,37283_at,40954_at,31758_at,36960_at,33143_s_at,37048_at,38538_at,1005_at,34963_at,39408_at,32464_at,706_at,1276_g_at,164_at,41445_at,40735_at,1891_at,1258_s_at,40856_at,1911_s_at,31562_at,32359_at,274_at,1804_at,41387_r_at,848_at,41499_at,39448_r_at,34537_at,36459_at,35500_at,37139_at,612_s_at,32133_at,39757_at,37629_at,38463_s_at,568_at,749_at,1939_at,38018_g_at,1857_at,32699_s_at,40661_at,1994_at,38373_g_at,33893_r_at,1388_g_at,35345_at,1385_at,36615_at,1263_at,37385_at,1774_at,37233_at,39753_at,32626_at,35915_at,35714_at,31669_s_at,36519_at,40473_at,1750_at,33751_at,37831_at,35472_at,41825_at,34666_at,35471_g_at,31888_s_at,37722_s_at,35414_s_at,39750_at,35726_at,37662_at,33802_at,352_at,31737_at,37938_at,36161_at,31558_at,34475_at,37223_at,38953_at,37857_at,189_s_at,41169_at,33092_at,38660_at,40895_g_at,37146_at,1936_s_at,38860_at,40210_at,41180_i_at,31586_f_at,33366_at,31521_f_at,762_f_at,1124_at,36009_at,41111_at,36749_at,37310_at,31522_f_at,35768_at,39421_at,39967_at,35992_at,38356_at,39331_at,34145_at,35378_at,199_s_at,35966_at,1866_g_at,37377_i_at,37378_r_at,833_at,31586_f_at,38062_at,34981_at,1569_r_at,1548_s_at,41446_f_at,36999_at,34226_at,33385_g_at,36173_r_at,1007_s_at,35149_at,38671_at,1973_s_at,37724_at,37317_at,33829_at,36532_at,39372_at,41717_at,38221_at,37418_at,33120_at,136_at,33492_at,1602_at,41505_r_at,41736_g_at,37862_at,31859_at,40913_at,35956_s_at,32193_at,1148_s_at,1244_at,38684_at,37440_at,32186_at,1242_at,39503_s_at,224_at,38374_at,36018_at,36603_at,33288_i_at,33662_at,33555_at,33539_at,430_at,471_f_at,1369_s_at,35372_r_at,38089_at,40310_at,41106_at,41216_r_at,32815_at,37463_r_at,33470_at,40522_at,1463_at,1743_s_at,1895_at,32583_at,35440_g_at,1091_at,1649_at,287_at,32119_at,131_at,38642_at,33922_at,35886_at,38326_at,38823_s_at,41088_at,41371_at,39841_at,32486_at,41234_at,41598_at,40478_at,37606_at,37170_at,34857_at,32062_at,37762_at,36052_at,40442_f_at,41550_at,36621_at,36929_at,38645_at,34438_at,39587_at,36562_at,37155_at,36055_at,36754_at,33545_at,1520_s_at,39402_at,32265_at,32679_at,1829_at,40669_at,31694_at,41382_at,41446_f_at,38391_at,34560_at,40098_at,32522_f_at,988_at,789_at,1270_at,1139_at,33665_s_at,1237_at,412_s_at,34688_at,31353_f_at,41856_at,32928_at,37584_at,32379_f_at,936_s_at,2082_s_at,36479_at,39175_at,32007_at,36103_at,37270_at,40840_at,37206_at,37365_at,37820_at,35848_at,37111_g_at,39522_at,36760_at,35018_at,31745_at,37424_at,36507_at,719_g_at,34165_at,41850_s_at';
 my $idType = 'AFFYMETRIX_3PRIME_IVT_ID';
 my $listName = 'make_up';
 my $listType=0;
 #to add background list, set listType=1
 my $list = $soap ->addList($inputIds, $idType, $listName, $listType)->result;
 print "\n$list of list was mapped\n"; 
  	
 #list all species  names
 my $allSpecies= $soap ->getSpecies()->result;	 	  	
 # print  "\nAll species: \n$allSpecies\n"; 
 #list current species  names
 my $currentSpecies= $soap ->getCurrentSpecies()->result;	 	  	
 #print  "\nCurrent species: \n$currentSpecies\n"; 

 #set user defined species 
 #my $species = $soap ->setCurrentSpecies("1")->result;

 #print "\nCurrent species: \n$species\n"; 
 
#set user defined categories 
#my $categories = $soap ->setCategories("BBID,BIOCARTA,COG_ONTOLOGY,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,UP_SEQ_FEATURE")->result;
#to user DAVID default categories, send empty string to setCategories():
 my $categories = $soap ->setCategories("")->result;
#print "\nValid categories: \n$categories\n\n";  
 
open (chartReport, ">", "chartReport.txt");
print chartReport "Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n";
#close chartReport;

#open (chartReport, ">>", "chartReport.txt");
#getChartReport 	
my $thd=0.1;
my $ct = 2;
my $chartReport = $soap->getChartReport($thd,$ct);
	my @chartRecords = $chartReport->paramsout;
	#shift(@chartRecords,($chartReport->result));
	#print $chartReport->result."\n";
  	print "Total chart records: ".(@chartRecords+1)."\n";
  	print "\n ";
	#my $retval = %{$chartReport->result};
	my @chartRecordKeys = keys %{$chartReport->result};
	
	#print "@chartRecordKeys\n";
	
	my @chartRecordValues = values %{$chartReport->result};
	
	my %chartRecord = %{$chartReport->result};
	my $categoryName = $chartRecord{"categoryName"};
	my $termName = $chartRecord{"termName"};
	my $listHits = $chartRecord{"listHits"};
	my $percent = $chartRecord{"percent"};
	my $ease = $chartRecord{"ease"};
	my $Genes = $chartRecord{"geneIds"};
	my $listTotals = $chartRecord{"listTotals"};
	my $popHits = $chartRecord{"popHits"};
	my $popTotals = $chartRecord{"popTotals"};
	my $foldEnrichment = $chartRecord{"foldEnrichment"};
	my $bonferroni = $chartRecord{"bonferroni"};
	my $benjamini = $chartRecord{"benjamini"};
	my $FDR = $chartRecord{"afdr"};
	
	print chartReport "$categoryName\t$termName\t$listHits\t$percent\t$ease\t$Genes\t$listTotals\t$popHits\t$popTotals\t$foldEnrichment\t$bonferroni\t$benjamini\t$FDR\n";
	
	
	for $j (0 .. (@chartRecords-1))
	{			
		%chartRecord = %{$chartRecords[$j]};
		$categoryName = $chartRecord{"categoryName"};
		$termName = $chartRecord{"termName"};
		$listHits = $chartRecord{"listHits"};
		$percent = $chartRecord{"percent"};
		$ease = $chartRecord{"ease"};
		$Genes = $chartRecord{"geneIds"};
		$listTotals = $chartRecord{"listTotals"};
		$popHits = $chartRecord{"popHits"};
		$popTotals = $chartRecord{"popTotals"};
		$foldEnrichment = $chartRecord{"foldEnrichment"};
		$bonferroni = $chartRecord{"bonferroni"};
		$benjamini = $chartRecord{"benjamini"};
		$FDR = $chartRecord{"afdr"};			
		print chartReport "$categoryName\t$termName\t$listHits\t$percent\t$ease\t$Genes\t$listTotals\t$popHits\t$popTotals\t$foldEnrichment\t$bonferroni\t$benjamini\t$FDR\n";				 
	}		  	
	
	close chartReport;
	print "\nchartReport.txt generated\n";
} 
__END__
		
=cut
