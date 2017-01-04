# coding=utf-8
"""光谱指数"""
import statistics


def ndvi(bands):
    """
    计算NDVI
    公式采用ndvi=(r831-r667)/(r831+r667)
    @param bands 高光谱波段数据
    @return NDVI
    """
    return (bands[481] - bands[317])/(bands[481] + bands[317])


def pri(bands):
    """
    计算光化学植被指数(photochemical reflectance index, PRI)
    不同的植被不同的PRI，用于指示光合作用能力、光能利用能力、
    水分胁迫。Gamon et al. Relationshhips between NDVI, canopy
    structure, and photosynthesis in 3 Californian vegetation
    types. 1995
    PRI = (r531-r570)/(r531+r570)
    @param bands 高光谱波段数据
    @return PRI
    """
    return round((bands[181] - bands[220]) / (bands[181] + bands[220]), 6)


def gm1(bands):
    """
    与叶片叶绿素(chlorophyII) 1含量相关. Gitelson A A, Merzlyak M N.
    Remote estimation of chlorophyII content in higher plant leaves.
    1997.
    gm1 = r750/550
    @param 高光谱数据
    @return gm1
    """
    return round(bands[450] / bands[250], 6)


def gm2(bands):
    """
    叶绿素2含量相关
    gm2 = r750/700
    """
    return round(bands[450] / bands[400], 6)


def lic1(bands):
    """
    侦测绿色植物叶片的胁迫. Lichtenthaler et al. Detection of vegetation
    stress via a new high resolution fluorescence imaging system. 1996
    lic1 = (r800-r680)/(r800+r680)
    lic2 = r440/r690
    lic3 = r440/r740
    """
    return (bands[450] - bands[330])/(bands[450] + bands[330])


def lic2(bands):
    """lic2"""
    return round(bands[90] / bands[340], 6)


def lic3(bands):
    """ lic3 """
    return round(bands[90] / bands[390], 6)


def srpi(bands):
    """
    简单色素比较指数(simple ratio pigment index, SRPI), 该指数基于叶片
    类胡萝卜素和叶绿素含量. Penuelas et al.Semi-imperical indices to
    assess carotenoids/chlorophyII, a ratio from leaf spectral
    reflectance. 1995
    srpi = r430/r680
    """
    return round(bands[80] / bands[330], 6)


def npi(bands):
    """
    归一化脱镁叶绿素指数(Normalized phaepophytiniz index, npi), Barnes et al.
    A reappraisal of the use of DMSO for the extraction and determination of
    chlorophylls a and b in lichens and higher plants. 1992
    npi = (r415-r435)/(r415+r435)
    """
    return round((bands[65] - bands[85]) / (bands[65] + bands[85]), 6)


def npcri(bands):
    """
    归一化叶绿素比例指数(Normalized pigment chlorophyll ratio index, npcri)
    Penuelas et al. Reflectance indices associated with physiological changes
    in nitrogen- and water-limited sunflower leaves. 1994
    npcri = (r680-r430)/(r680+r430)
    """
    return round((bands[330] - bands[80]) / (bands[330] + bands[80]), 6)


def gi(bands):
    """
    绿度指数(Greenness index, GI).
    gi =  r554/r677
    """
    return round(bands[204] / bands[327], 6)


def sipi(bands):
    """
    structure intensive pigment index, sipi. Penuelas and Filella. Visible and
    near-infrared reflectance techniques for diagnosing plant physiological
    status.2002
    sipi = (r445-r800)/(r680-r800)
    """
    return round((bands[95] - bands[450]) / (bands[330] - bands[450]), 6)


def sr(bands):
    """
    Simple Ratio, sr. indicator of prolonged vegetation stress due to changes
    in canopy structrue. Gong et al. Analysis of in situ hyperspectral data
    for nutrient estimation of giant sequoia. 2002
    sr = r774/r677
    """
    return round(bands[424] / bands[327], 6)


def wi(bands):
    """
    water index, wi. water status. Penuelas et al. Estimation of plant water
    concentration by the reflectance water index WI(r900/r970). 1997
    wi = r900/r970
    """
    return round(bands[550] / bands[620], 6)


def cai(bands):
    """
    cellulose absorption index, cai. water status. Nagler et al. Cellulose
    absorption index (CAI) to quantify mixed soil-plant litter scenes. 1997
    cai = 0.5*(r2000+r2200)-r2100.
    """
    return round(0.5*(bands[1650] + bands[1850]) - bands[1750], 6)


def msi(bands):
    """
    moisture stress index. water status. Rock et al. Remote detection of forest
    damage. 1986.
    msi = r1600/r820
    """
    return round(bands[1250] / bands[470], 6)


def ndwi(bands):
    """
    normalized difference water index, ndwi. water status. Gao et al. NDWI- A
    normalized difference water index for remote sensing of vegetation liquid
    water from space. 1996.
    ndwi = (r860-r1240)/(r860+r1240)
    """
    return round((bands[510]-bands[690]) / (bands[510]+bands[690]), 6)


def dwsi(bands):
    """
    disease water stress index. dwsi. water status. Galvao et al.
    Discrimination of sugarcane varieties in southeastern Brazil
    with EO-1 hyperion data. 2005
    dwsi = (r802+r547)/(r1657+r682)
    """
    return round((bands[452] + bands[297]) / (bands[1307]+bands[332]), 6)


def ratio975(bands):
    """
    3-bands ratio at 975. water status. Pu et al. Spectral absorption features
    as indicators of water satus in coast live oak(Quercus agrifolia) leaves.
    2003
    ratio975=2*r960-990/(r920-940 + r1090-1110)
    """
    temp1 = statistics.mean(bands[610:641])
    temp2 = statistics.mean(bands[570:591])
    temp3 = statistics.mean(bands[740:761])
    return round(2 * temp1 / (temp2 + temp3), 6)


def ratio1200(bands):
    """
    ratio1200 = 2*r1180-1200/(r1090-1110 + r1265-1285)
    """
    temp1 = statistics.mean(bands[830:851])
    temp2 = statistics.mean(bands[740:761])
    temp3 = statistics.mean(bands[915:936])
    return round(2 * temp1 / (temp2 + temp3), 6)


def lci(bands):
    """
    Leaf Chlorophyll index, lci. Datt. Visible/near infraed reflectance and
    chlorophyll content in eucalyptus leaves. 1999
    lci = (r850-r710)/(r850+r710)
    """
    return round((bands[500] - bands[360]) / (bands[500] + bands[360]), 6)


def sga(bands):
    """
    chlorophyll index. Sims and Gamon. relationships between leaf pigment
    content and spectral reflectance across a wide range of species. 2002
    sga = (r750+r705)/(r750+r705-2*r445)
    """
    return round((bands[400] + bands[355]) / (bands[400] + bands[355] - 2 * bands[95]), 6)


def sgb(bands):
    """
    chlorophyll index.
    sgb = (r750 - r445)/(r705 - r445)
    """
    return round((bands[400] - bands[95]) / (bands[355] - bands[95]), 6)


def wi1180(bands):
    """
    water index at 1180nm. Sims and Gamon. Estimation of vegetation water
    content and photosynthetic tissue area from spectral reflectance: a
    comparison of indices based on liquid water and chlorophyll absorption
    features. 2003
    wi1180 = r900/r1180
    """
    return round(bands[550] / bands[830], 6)
