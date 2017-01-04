# coding=utf-8
import numpy as np
import pandas as pd
from sklearn import preprocessing


def relate_calculate(specfile, biofile, savefile):
    """
    =====================
    specfile文件格式应该如下:
    bands, s1, s2, s3,...
    350,   0.111, 0.112, 0.113,...
    ....
    =====================
    biofile文件格式如下:
    bioName, s1, s2, s3,...
    氨基酸, 0.44, 0.55, 0.66
    糖分, ........
    =====================
    savefile的保存格式为:
    bands, 氨基酸, 糖分,...
    .......
    """
    try:
        specdata = pd.read_csv(specfile, index_col=0)
        biodata = pd.read_csv(biofile, index_col=0)
    except Exception as e:
        print("relate_calculate: %s" % e)
        return False

    res = correlation(specdata.values, biodata.values)
    bandindex = specdata.index
    filedname = list(biodata.index)
    try:
        kk = pd.DataFrame(data=res, index=bandindex, columns=filedname)
        kk.to_csv(savefile)
    except Exception as e:
        print("relate_calculate: %s" % e)
        return False
    return True


def correlation(spec, bio):
    """
    计算相关系数
    spec为光谱数据
    bio为相应的生化参数
    """
    spec = np.array(spec)
    bio = np.array(bio)
    if bio.shape[1] != spec.shape[1]:
        print("输入数据无效, 样本数不一致。")
        return None
    # 获取bio行数
    cols = bio.shape[0]
    # 获取spec行数
    rows = spec.shape[0]
    res = [[] for col in range(cols)]
    for col in range(cols):
        biomean = np.mean(bio[col])
        biodelta = bio[col] - biomean
        biodeltasq = np.sum(np.multiply(biodelta, biodelta)) ** 0.5
        for row in range(rows):
            bandmean = np.mean(spec[row])
            banddelta = spec[row] - bandmean
            banddeltasq = np.sum(np.multiply(banddelta, banddelta)) ** 0.5
            deltam = np.sum(np.multiply(biodelta, banddelta))
            rel = np.divide(deltam, banddeltasq * biodeltasq)
            res[col].append(rel)
    res = np.array(res).T
    return res


class PCA:
    def __init__(self, n_components=None, standardization=True, copy=True):
        """
        param n_components: 最后要保留的成分数目
        param standardization: 是否要数据标准化
        param copy: 是否要复制数据
        """
        self.n_components = n_components
        self.standardization = standardization
        self.copy = copy
        self.cov = None
        self.eigenvalues = None
        self.eigenvector = None

    def fit(self, x):
        """
        param x: (样本数, 特征数) 的数据
        """
        if self.copy:
            x = np.copy(x)
        if self.standardization:
            x = preprocessing.scale(x)
        x = np.array(x)
        covmat = np.corrcoef(x.T)
        self.cov = covmat
        self.eigenvalues, self.eigenvector = np.linalg.eig(covmat)
        self.loadings = np.multiply(self.eigenvalues.real**0.5,
                                    self.eigenvector)
        
        n_c = min(x.shape)
        if self.n_components is None:
            self.n_components = n_c
        elif self.n_components > n_c:
            self.n_components = n_c

        sum_eigvalue = np.sum(self.eigenvalues.real)
        self.percent = self.eigenvalues/sum_eigvalue
        self.percent = self.percent[: self.n_components]
        self.eigenvalues = self.eigenvalues[: self.n_components]
        self.eigenvector = self.eigenvector.real[:, : self.n_components]
        self.loadings = self.loadings[:, : self.n_components]

    def get_covariance(self):
        return self.cov

    def get_eigenvalues(self):
        return self.eigenvalues

    def get_eigenvector(self):
        return self.eigenvector

    def get_loadings(self):
        """
        获取载荷矩阵
        """
        return self.loadings.real

    def get_percent(self):
        """
        获取组分贡献比例
        """
        return self.percent

    def transform(self, x):
        """
        把数据转换到主成分空间
        """
        try:
            data = np.dot(x, self.eigenvector)
            return data
        except ValueError as err:
            print(err)