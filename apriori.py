def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:#遍历数据集中的每一条交易
        for item in transaction:#遍历每一条交易中的每个商品
            if not [item] in C1:
                C1.append([item])

    C1.sort()
    return map(frozenset, C1)  # use frozen set so we
    # can use it as a key in a dict 即不可改变


#扫描数据集D，观察每个候选集Ck在D中出现的支持度计数
#该函数用于从C1生成L1，L1表示满足最低支持度的元素集合
def scanD(D, Ck, minSupport):
    ssCnt = {}#创建空字典ssCnt
    for tid in D:#数据集D中每一条记录tid
        for can in Ck:#候选集Ck中的每个集合can
            # issubset：表示如果集合can中的每一元素都在tid中则返回true
            if can.issubset(tid):#如果某个集合can在D中某一条记录tid中出现了
                if not ssCnt.has_key(can):#如果字典ssCnt中的键没有can这个集合
                    ssCnt[can] = 1#就做这一步，值为1
                else:#在这里，字典中的key(键)：就是can集合，(value)值就是这个集合的计数
                    ssCnt[can] += 1#如果已经有这个集合了，计数加1
    numItems = float(len(D))#计数D中所有记录的条数
    retList = []
    supportData = {}
    for key in ssCnt:#对于ssCnt中所有的键(也就是每个项集)，进行如下操作，计算支持度
        support = ssCnt[key] / numItems
        if support >= minSupport:#如果大于最小支持度，则将该项集加入retList列表中
            retList.insert(0, key)#从列表的首部插入任意一个新的集合
        supportData[key] = support#构建支持的项集的字典，key是项集，value是计算出来的支持度
    return retList, supportData#返回这个列表和这个集合

def aprioriGen(Lk,k):#creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range (i+1,lenLk):
            L1 = list(Lk[i])[:k-2];L2 = list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet,minSupport = 0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D,C1,minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2])>0):
        Ck = aprioriGen(L[k-2],k)
        Lk,supk = scanD(D,Ck,minSupport)
        supportData.update(supk)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L,supportData,minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if(i>1):
                rulesFromConseq(freqSet,H1,supportData, bigRuleList,\
                                minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

#对生成的候选规则集合进行评估
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            print freqSet-conseq,'-->',conseq,'conf:',conf
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

#生成候选规则集合
def rulesFromConseq(freqSet, H, supportData, brl, minConf= 0.7):
    m = len(H[0])
    if (len(freqSet) > (m+1)):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if(len(Hmp1)>1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)






