from algotaf.backend.fileio import db_host, sensitive_data, nasdaq, amex, nyse


def chunks(l, n):
    big_list = []
    n = max(1, n)
    step = int(len(l) / n)
    for i in range(0, len(l), step):
        big_list.append(l[i:i+step])
    return big_list


DB_NAME = 'algotaf'

USERNAME = sensitive_data.USERNAME
PASSWORD = sensitive_data.PASSWORD
HOSTNAME = db_host.DB_HOST
BACKUP_HOSTNAME = 'localhost'


TICKERS_TEMP = ['abt', 'abbv', 'acn', 'ace', 'adbe', 'adt', 'aap',
           'aes', 'aet', 'afl', 'amg', 'a', 'gas', 'apd', 'arg',
           'akam', 'aa', 'agn', 'alxn', 'alle', 'ads', 'all', 'altr',
           'mo', 'amzn', 'aee', 'aal', 'aep', 'axp', 'aig', 'amt',
           'amp', 'abc', 'ame', 'amgn', 'aph', 'apc', 'adi', 'aon',
           'apa', 'aiv', 'amat', 'adm', 'aiz', 't', 'adsk', 'adp', 'an',
           'azo', 'avgo', 'avb', 'avy', 'bhi', 'bll', 'bac', 'bk', 'bcr',
           'bxlt', 'bax', 'bbt', 'bdx', 'bbby', 'brk-b', 'bby', 'blx',
           'hrb', 'ba', 'bwa', 'bxp', 'bsk', 'bmy', 'brcm', 'bf-b',
           'chrw', 'ca', 'cvc', 'cog', 'cam', 'cpb', 'cof', 'cah', 'hsic',
           'kmx', 'ccl', 'cat', 'cbg', 'cbs', 'celg', 'cnp', 'ctl', 'cern',
           'cf', 'schw', 'chk', 'cvx', 'cmg', 'cb', 'ci', 'xec', 'cinf',
           'ctas', 'csco', 'c', 'ctxs', 'clx', 'cme', 'cms', 'coh', 'ko',
           'cce', 'ctsh', 'cl', 'cmcsa', 'cma', 'csc', 'cag', 'cop', 'cnx',
           'ed', 'stz', 'glw', 'cost', 'cci', 'csx', 'cmi', 'cvs', 'dhi',
           'dhr', 'dri', 'dva', 'de', 'dlph', 'dal', 'xray', 'dvn', 'do',
           'dtv', 'dfs', 'disca', 'disck', 'dg', 'dltr', 'd', 'dov', 'dow',
           'dps', 'dte', 'dd', 'duk', 'dnb', 'etfc', 'emn', 'etn', 'ebay',
           'ecl', 'eix', 'ew', 'ea', 'emc', 'emr', 'endp', 'esv', 'etr',
           'eog', 'eqt', 'efx', 'eqix', 'eqr', 'ess', 'el', 'es', 'exc',
           'expe', 'expd', 'esrx', 'xom', 'ffiv', 'fb', 'fast', 'fdx', 'fis',
           'fitb', 'fslr', 'fe', 'fsiv', 'flir', 'fls', 'flr', 'fmc', 'fti',
           'f', 'fosl', 'ben', 'fcx', 'ftr', 'gme', 'gps', 'grmn', 'gd', 'ge',
           'ggp', 'gis', 'gm', 'gpc', 'gnw', 'gild', 'gs', 'gt', 'googl', 'goog',
           'gww', 'hal', 'hbi', 'hog', 'har', 'hrs', 'hig', 'has', 'hca', 'hcp',
           'hcn', 'hp', 'hes', 'hpq', 'hd', 'hon', 'hrl', 'hsp', 'hst', 'hcbk',
           'hum', 'hban', 'itw', 'ir', 'intc', 'ice', 'ibm', 'ip', 'ipg', 'iff',
           'intu', 'isrg', 'ivz', 'irm', 'jec', 'jbht', 'jnj', 'jci', 'joy', 'jpm',
           'jnpr', 'ksu', 'k', 'key', 'gmcr', 'kmb', 'kim', 'kmi', 'klac', 'kss',
           'krft', 'kr', 'lb', 'lll', 'lh', 'lrcx', 'lm', 'leg', 'len', 'lvlt',
           'luk', 'lly', 'lnc', 'lltc', 'lmt', 'l', 'low', 'lyb', 'mtb', 'mac',
           'm', 'mnk', 'mro', 'mpc', 'mar', 'mmc', 'mlm', 'mas', 'ma', 'mat',
           'mkc', 'mcd', 'mhfi', 'mck', 'mjn', 'mmv', 'mdt', 'mrk', 'met',
           'kors', 'mchp', 'mu', 'msft', 'mhk', 'tap', 'mdlz', 'mon', 'mnst',
           'mco', 'ms', 'mos', 'msi', 'mur', 'myl', 'ndaq', 'nov', 'navi',
           'ntap', 'nflx', 'nwl', 'nfx', 'nem', 'nwsa', 'nee', 'nlsn',
           'nke', 'ni', 'ne', 'nbl', 'jwn', 'nsc', 'ntrs', 'noc', 'nrg',
           'nue', 'nvda', 'orly', 'oxy', 'omc', 'oke', 'orcl', 'oi', 'pcar',
           'pll', 'ph', 'pdco', 'payx', 'pnr', 'pbct', 'pom', 'pep', 'pki',
           'prgo', 'pfe', 'pcg', 'pm', 'psx', 'pnw', 'pxd', 'pbi', 'pcl',
           'pnc', 'rl', 'ppg', 'ppl', 'px', 'pcp', 'pcln', 'pfg', 'pg',
           'pgr', 'pld', 'pru', 'peg', 'psa', 'phm', 'pvh', 'qrvo', 'pwr',
           'qcom', 'dgx', 'rrc', 'rtn', 'o', 'rht', 'regn', 'rf', 'rsg',
           'rai', 'rhi', 'rok', 'col', 'rop', 'rost', 'rlc', 'r', 'crm',
           'sndk', 'scg', 'slb', 'sni', 'stx', 'see', 'sre', 'shw', 'sial',
           'spg', 'swks', 'slg', 'sjm', 'sna', 'so', 'luv', 'swn', 'se',
           'stj', 'swk', 'spls', 'sbux', 'hot', 'stt', 'srcl', 'syk', 'sti',
           'symc', 'syy', 'trow', 'tgt', 'tel', 'te', 'tgna', 'thc', 'tdc',
           'tso', 'txn', 'txt', 'hsy', 'trv', 'tmo', 'tif', 'twx', 'twc',
           'tjk', 'tmk', 'tss', 'tsco', 'rig', 'trip', 'foxa', 'tsn',
           'tyc', 'ua', 'unp', 'unh', 'ups', 'uri', 'utx', 'uhs', 'unm',
           'urbn', 'vfc', 'vlo', 'var', 'vtr', 'vrsn', 'vz', 'vrtx', 'viab',
           'v', 'vno', 'vmc', 'wmt', 'wba', 'dis', 'wm', 'wat', 'antm', 'wfc',
           'wdc', 'wu', 'wy', 'whr', 'wfm', 'wmb', 'wec', 'wyn', 'wynn', 'xel',
           'xrx', 'xlnx', 'xl', 'xyl', 'yhoo', 'yum', 'zbh', 'zion', 'zts']

ALL_TICKERS = ['TXG','YI','PIH','PIHPP','TURN','FLWS','BCOW','ONEM','FCCY','SRCE','VNET','TWOU','QFIN','KRKR',
           'JOBS','ETNB','JFK','JFKKR','JFKKU','JFKKW','EGHT','NMTR','JFU','AAON','ABEO','ABMD','AXAS',
           'ACIU','ACIA','ACTG','ACHC','ACAD','ACAM','ACAMU','ACAMW','ACST','AXDX','ACCP','XLRN','ARAY',
           'ACRX','ACER','ACHV','ACIW','ACRS','ACMR','ACNB','ACOR','ACTT','ACTTU','ACTTW','ATVI','ADMS',
           'ADMP','AHCO','ADAP','ADPT','ADXN','ADUS','AEY','IOTS','ADIL','ADILW','ADMA','ADBE','ADTN',
           'ADRO','ADES','AEIS','AMD','ADXS','ADVM','DWEQ','DWAW','DWUS','DWMC','DWSH','ACT','AEGN','AGLE',
           'AEHR','AMTX','AERI','AVAV','ARPO','AIH','AEZS','AEMD','AFMD','AFYA','AGBA','AGBAR','AGBAU',
           'AGBAW','AGEN','AGRX','AGYS','AGIO','AGMH','AGNC','AGNCM','AGNCN','AGNCO','AGNCP','AGFS',
           'AGFSW','AIKI','ALRN','AIMT','AIRT','AIRTP','AIRTW','ATSG','AIRG','ANTE','AKAM','AKTX',
           'AKCA','AKBA','KERN','KERNW','AKRO','AKER','AKTS','ALRM','ALSK','ALAC','ALACR','ALACU',
           'ALACW','ALBO','ALDX','ALEC','ALRS','ALXN','ALCO','ALIT','ALGN','ALIM','ALYA','ALJJ','ALKS',
           'ALLK','ABTX','ALGT','ALNA','ARLP','LNT','AESE','AHPI','AMOT','ALLO','ALLT','MDRX','ALNY',
           'AOSL','GOOG','GOOGL','SMCP','ATEC','ALPN','ALTR','ATHE','ALT','ASPS','AIMC','ALTM','AMAG',
           'AMAL','AMRN','AMRK','AMZN','AMBC','AMBA','AMCX','AMCI','AMCIU','AMCIW','DOX','AMED','AMTB',
           'AMTBB','UHAL','AMRH','AMRHW','ATAX','AMOV','AAL','AFIN','AFINP','AMNB','ANAT','APEI','AREC',
           'AMRB','AMSWA','AMSC','AVCT','AVCTW','AMWD','CRMT','ABCB','AMSF','ASRV','ASRVP','ATLO','AMGN',
           'FOLD','AMKR','AMPH','IBUY','AMHC','AMHCU','AMHCW','ASYS','AMRS','ADI','ANAB','AVXL','ANCN',
           'ANDA','ANDAR','ANDAU','ANDAW','ANGI','ANGO','ANIP','ANIK','ANIX','ANPC','ANSS','ATRS','ATEX',
           'APA','APLS','APEX','APXT','APXTU','APXTW','APHA','APOG','APEN','AINV','AMEH','APPF','APPN',
           'AAPL','APDN','AGTC','AMAT','AMTI','AAOI','APLT','APRE','APVO','APTX','APM','APTO','APYX',
           'AQMS','AQB','AQST','ARAV','ABUS','ABIO','RKDA','ARCB','ACGL','ACGLO','ACGLP','FUV','ARCE',
           'ARCT','ARQT','ARDX','ARNA','ARCC','ARGX','ARDS','ARKR','DWCR','DWAT','AROW','ARWR','ARTL',
           'ARTLW','ARTNA','ARTW','ARVN','ARYBU','ARYA','ARYAU','ARYAW','ASNA','ASND','APWC','ASLN','ASML',
           'ASPU','AZPN','AWH','ASMB','ASRT','ASFI','ASTE','ATRO','ALOT','ASTC','ASUR','AACG','ATRA',
           'ATNX','ATHX','ATIF','AAME','ACBI','AUB','AUBAP','AY','ATLC','AAWW','AFH','ATCX','ATCXW',
           'TEAM','ATNI','ATOM','ATOS','BCEL','ATRC','ATRI','LIFE','AUBN','AUDC','AEYE','AUPH','EARS',
           'JG','ADSK','AUTL','ADP','AUTO','AVDL','AHI','AVCO','ATXI','AVEO','AVNW','CDMO','CDMOP',
           'AVID','RNA','AVGR','CAR','RCEL','AVT','AVRO','AWRE','ACLS','AXLA','AXGN','AAXN','AXNX',
           'AXGT','AXSM','AXTI','AYLA','AYRO','AYTU','AZRX','BCOM','RILY','RILYG','RILYH','RILYI',
           'RILYM','RILYN','RILYO','RILYP','RILYZ','BOSC','BIDU','BCPC','BLDP','BANF','BANFP','BCTF',
           'BAND','BFC','BOCH','BMRC','BMLP','BKSC','BOTJ','OZK','BSVN','BFIN','BWFG','BANR','BZUN',
           'DFVL','DFVS','DTUL','DTUS','DTYL','FLAT','STPP','TAPR','BBSI','GOLD','BSET','ZTEST','BXRX',
           'BCML','BBQ','BCBP','BECN','BEAM','BBGI','BBBY','BGNE','BELFA','BELFB','BLPH','BLCM','BLU',
           'BNFT','BFYT','BNTC','BRY','BWMX','XAIR','BYND','BYSI','BGCP','BCYC','BGFV','BRPA','BRPAR',
           'BRPAU','BRPAW','BILI','BASI','BCDA','BCDAW','BIOC','BCRX','BDSI','BFRA','BIIB','BHTG','BKYI',
           'BIOL','BLFS','BLRX','BMRN','BMRA','BNGO','BNGOW','BVXV','BNTX','BPTH','BSGM','BSTC','TECH',
           'BEAT','BIVI','BTAI','BJRI','BDTX','BLKB','BL','BKCC','TCPC','BLNK','BLNKW','BLMN','BCOR',
           'BLBD','BHAT','BLUE','BKEP','BKEPP','BPMC','ITEQ','BMCH','BSBK','WIFI','BOKF','BOKFL','BNSO',
           'BKNG','BIMI','BRQS','BOMN','BPFH','EPAY','BOXL','BBRX','BCLI','BWAY','BCTX','BBI','BDGE',
           'BBIO','BLIN','BWB','BRID','BCOV','BHF','BHFAL','BHFAO','BHFAP','AVGO','AVGOP','BYFC','BWEN',
           'BROG','BROGW','BPY','BPYPN','BPYPO','BPYPP','BPYU','BPYUP','BRKL','BRKS','BRP','DOOO','BRKR',
           'BMTC','BSQR','BLDR','BNR','BFST','CFFI','CHRW','CABA','CCMP','CDNS','CDZI','CZR','CSTE',
           'CLBS','CHY','CHI','CCD','CHW','CGO','CPZ','CSQ','CAMP','CVGW','CALB','CALA','CALT','CALM',
           'CLMT','CLXT','CMBM','CATC','CAC','CAMT','CAN','CSIQ','CGIX','CPHC','CBNK','CCBG','CPLP',
           'CSWC','CSWCL','CPTA','CPTAG','CPTAL','CFFN','CAPR','CSTR','CPST','CARA','CRDF','CSII','CDLX',
           'CATM','CDNA','CTRE','CARG','TAST','CARE','CARV','CASA','CWST','CASY','CASI','CASS','SAVA',
           'CSTL','CTRM','CATB','CBIO','CPRX','CATS','CATY','CVCO','CBFV','CBAT','CBMB','CBOE','CBTX',
           'CDK','CDW','CECE','CELC','CLDX','APOP','APOPW','CLRB','CLRBZ','CLLS','CBMG','CLSN','CELH',
           'CYAD','CETX','CETXP','CETXW','CDEV','CNTG','CETV','CFBK','CENT','CENTA','CVCY','CNTX','CENX',
           'CNBKA','CNTY','CRNT','CERC','CRNC','CERN','CERS','CEVA','CFFA','CFFAU','CFFAW','CSBR','CHNG',
           'CHNGU','CTHR','GTLS','CHTR','CHKP','CHEK','CHEKZ','CKPT','CEMI','CCXI','CHMG','CHFS','CHMA',
           'CSSE','CSSEP','PLCE','CMRX','CAAS','CBPO','CCCL','CCRC','JRJC','HGSH','CIH','CJJD','CLEU',
           'CHNR','CREG','SXTC','CXDC','PLIN','CNET','IMOS','COFS','CHPM','CHPMU','CHPMW','CDXC','CHSCL',
           'CHSCM','CHSCN','CHSCO','CHSCP','CHDN','CHUY','CDTX','CIIC','CIICU','CIICW','CMCT','CMCTP',
           'CMPR','CNNB','CINF','CIDM','CTAS','CRUS','CSCO','CTRN','CTXR','CTXRW','CZNC','CZWI','CIZN',
           'CTXS','CHCO','CIVB','CLAR','CLNE','CLSK','CACG','YLDE','LRGE','CLFD','CLRO','CLPT','CLSD',
           'CLIR','CBLI','CLVS','CLPS','CME','CCNE','CNSP','CCB','COKE','COCP','CODA','CCNC','CDXS',
           'CODX','CVLY','JVA','CCOI','CGNX','CTSH','CWBR','COHR','CHRS','COHU','CGROU','CLCT','COLL',
           'CIGI','CLGN','CBAN','HHT','COLB','CLBK','COLM','CMCO','CMCSA','CBSH','CBSHP','CVGI','COMM',
           'JCS','ESXB','CFBI','CTBI','CWBC','CVLT','CGEN','CPSI','CTG','SCOR','CHCI','CMTL','CNCE',
           'BBCP','CDOR','CNDT','CFMS','CNFR','CNFRL','CNMD','CNOB','CONN','CNSL','CWCO','CNST','ROAD',
           'CPSS','CFRX','CPTI','CPAA','CPAAU','CPAAW','CPRT','CRBP','CORT','CORE','CSOD','CRTX',
           'CLDB','CRVL','CRVS','CSGP','COST','CPAH','ICBK','COUP','CVTI','CVET','COWN','COWNL',
           'COWNZ','CPSH','CRAI','CBRL','BREW','CREX','CREXW','CACC','DGLD','DSLV','GLDI','SLVO',
           'TVIX','UGLD','USLV','USOI','VIIX','ZIV','CREE','CRSA','CRSAU','CRSAW','CCAP','CRESY',
           'CRNX','CRSP','CRTO','CROX','CRON','CCRN','CFB','CRWD','CRWS','CYRX','CYRXW','CSGS','CCLP',
           'CSPI','CSWI','CSX','CTIC','CUE','CPIX','CMLS','CRIS','CUTR','CVBF','CVV','CYAN','CYBR',
           'CYBE','CYCC','CYCCP','CYCN','CBAY','CYRN','CONE','CYTK','CTMX','CTSO','DADA','DJCO','DAKT',
           'DARE','DRIO','DRIOW','DZSI','DSKE','DSKEW','DAIO','DDOG','DTSS','PLAY','DTEA','DFNL','DINT',
           'DUSA','DWLD','DWSN','DBVT','DCPH','TACO','TACOW','DCTH','DBCP','DMPI','DNLI','DENN','XRAY',
           'DRMT','DMTK','DXLG','DSWL','DXCM','DFPH','DFPHU','DFPHW','DMAC','DHIL','FANG','DPHC','DPHCU',
           'DPHCW','DRNA','DFFN','DGII','DMRC','DRAD','DRADP','DGLY','APPS','DCOM','DCOMP','DIOD','DRTT',
           'DISCA','DISCB','DISCK','DISH','DHC','DHCNI','DHCNL','DLHC','BOOM','DOCU','DOGZ','DLTR',
           'DLPN','DLPNW','DOMO','DGICA','DGICB','DMLP','DORM','DOYU','DKNG','DKNGW','LYL','DBX','DSPG',
           'DLTH','DNKN','DUOT','DRRX','DXPE','DYAI','DYNT','DVAX','ETFC','SSP','EBMT','EGBN','EGLE',
           'EGRX','IGLE','ESSC','ESSCR','ESSCU','ESSCW','EWBC','EML','EAST','EVGBC','EVSTC','EVLMC',
           'EBAY','EBAYL','EBIX','ECHO','SATS','MOHO','EDAP','EDSA','EDNT','EDIT','EDUC','EGAN','EH',
           'EHTH','EIDX','EIGR','EKSO','LOCO','ESLT','ERI','SOLO','SOLOW','ECOR','EA','ELSE','ESBK',
           'ELOX','ELTK','EMCF','EMKR','ENTA','ECPG','WIRE','ENDP','ELGX','NDRA','NDRAW','EIGI','WATT',
           'EFOI','EHR','ERII','ENG','ENLV','ENOB','ENPH','ESGR','ESGRO','ESGRP','ETTX','ENTG','ENTX',
           'ENTXW','EBTC','EFSC','EVSI','EVSIW','EPZM','PLUS','EPSN','EQ','EQIX','EQBK','ERIC','ERIE',
           'ERYP','ESCA','ESPR','GMBL','GMBLW','ESQ','ESSA','EPIX','ESTA','VBND','VUSE','VIDI','ETON',
           'ETSY','CLWT','EDRY','EEFT','ESEA','EVLO','EVBG','EVK','EVER','MRAM','EVOP','EVFM','EVGN','EVOK',
           'EOLS','EVOL','EXAS','XGN','ROBO','XELA','EXEL','EXC','EXFO','XCUR','EXLS','EXPI','EXPE','EXPD',
           'EXPC','EXPCU','EXPCW','EXPO','STAY','XOG','EXTR','EYEG','EYEGW','EYEN','EYPT','EZPW','FLRZ',
           'FFIV','FB','FLMN','FLMNW','DUO','FANH','FARM','FMAO','FMNB','FAMI','FARO','FAST','FAT','FATE',
           'FBSS','FNHC','FENC','GSM','FFBW','FGEN','FDBC','ONEQ','FDUS','FDUSG','FDUSL','FDUSZ','FRGI',
           'FITB','FITBI','FITBO','FITBP','FISI','FNJN','FSRV','FSRVU','FSRVW','FTAC','FTACU','FTACW',
           'FEYE','FBNC','FNLC','FRBA','BUSE','FBIZ','FCAP','FCBP','FCNCA','FCNCP','FCBC','FCCO','FDEF',
           'FFBC','FFIN','THFF','FFNW','FFWM','FGBI','FHB','INBK','INBKL','INBKZ','FIBK','FRME','FMBH',
           'FMBI','FMBIP','FXNC','FNWB','FSFG','FSEA','FSLR','FAAR','FPA','BICK','FBZ','FTHI','FCAL','FCAN',
           'FTCS','FCEF','FCA','SKYY','RNDM','FDT','FDTS','FVC','FV','IFV','DDIV','DVOL','DVLU','DWPP',
           'DALI','FDNI','FEM','RNEM','FEMB','FEMS','FTSM','FEP','FEUZ','FGM','FTGC','FTLB','HYLS','FHK',
           'NFTY','FTAG','FTRI','LEGR','NXTG','FPXI','FPXE','FJP','FEX','FTC','RNLC','FTA','FLN','LMBS',
           'LDSF','FMB','FMK','FNX','FNY','RNMC','FNK','FAD','FAB','MDIV','MCEF','FMHI','QABA','ROBT','FTXO',
           'QCLN','GRID','CIBR','FTXG','CARZ','FTXN','FTXH','FTXD','FTXL','TDIV','FTXR','QQEW','QQXT','QTEC',
           'AIRR','RDVY','RFAP','RFDI','RFEM','RFEU','FID','FTSL','FYX','FYC','RNSC','FYT','SDVY','FKO',
           'FCVT','FDIV','FSZ','FIXD','TUSA','FKU','RNDV','FUNC','FUSB','MYFW','FCFS','SVVC','FSV','FISV',
           'FIVE','FPRX','FVE','FIVN','FLEX','FLXN','SKOR','MBSD','ASET','ESG','ESGG','LKOR','QLC','FPAY',
           'FLXS','FLIR','FLWR','FLNT','FLDM','FFIC','FLUX','FNCB','FOCS','FONR','FSCT','FRSX','FORM','FORTY',
           'FORR','FRTA','FTNT','FBIO','FBIOP','FMCI','FMCIU','FMCIW','FWRD','FORD','FWP','FOSL','FOX','FOXA',
           'FOXF','FRAN','FRG','FELE','FRAF','FRHC','RAIL','FEIM','FREQ','FRPT','FTDR','FRPH','FSBW','HUGE',
           'FTEK','FCEL','FULC','FLGT','FORK','FLL','FMAX','FULT','FNKO','FUTU','FTFT','FFHL','FVCB','WILC',
           'GTHX','GAIA','GLPG','GALT','GRTX','GLMD','GMDA','GLPI','GAN','GRMN','GARS','GLIBA','GLIBP','GDS',
           'GNSS','GENC','GFN','GFNCP','GFNSL','GBIO','GENE','GNFT','GNUS','GMAB','GNMK','GNCA','GNPX','GNTX',
           'THRM','GEOS','GABC','GERN','GEVO','ROCK','GIGM','GIII','GILT','GILD','GBCI','GLAD','GLADD',
           'GLADL','GOOD','GOODM','GOODN','GAIN','GAINL','GAINM','LAND','LANDP','GLBZ','GBT','ENT','GBLI',
           'GBLIL','GBLIZ','SELF','GWRS','AIQ','DRIV','POTX','CLOU','KRMA','BUG','DAX','EBIZ','FINX','CHIC',
           'GNOM','BFIT','SNSR','LNGR','MILN','EFAS','QYLD','BOTZ','CATH','SOCL','ALTY','SRET','GXTG','HERO',
           'YLCO','GLBS','GSMG','GSMGW','GLUU','GLYC','GOGO','GLNG','GMLP','GMLPP','DNJR','GDEN','GOGL',
           'GBDC','GTIM','GBLK','GSHD','GPRO','GPAQ','GPAQU','GPAQW','GHIV','GHIVU','GHIVW','GMHI','GMHIU',
           'GMHIW','GOSS','LOPE','GRVY','GECC','GECCL','GECCM','GECCN','GEC','GLDD','GSBC','GRBK','GPP','GPRE',
           'GCBC','GTEC','GNLN','GLRE','GRNQ','GNRS','GNRSU','GNRSW','GSKY','GRNV','GRNVR','GRNVU','GRNVW','GDYN',
           'GDYNW','GSUM','GRIF','GRFS','GRIN','GRTS','GO','GRPN','GRWG','OMAB','GGAL','GVP','GSIT','GTYH','GNTY',
           'GFED','GH','GHSI','GIFI','GURE','GPOR','GWPH','GWGH','GXGX','GXGXU','GXGXW','GYRO','HEES','HLG',
           'HNRG','HALL','HALO','HLNE','HJLI','HJLIW','HWC','HWCPL','HAFC','HAPP','HONE','HLIT','HARP','HROW',
           'HBIO','HCAP','HCAPZ','HAS','HA','HWKN','HWBK','HYAC','HYACU','HYACW','HAYN','HBT','HDS','HHR','HCAT',
           'HCCO','HCCOU','HCCOW','HCSG','HTIA','HQY','HSTM','HTLD','HTLF','HTBX','HEBT','HSII','HELE','HLIO',
           'HSDT','HMTV','HNNA','HCAC','HCACU','HCACW','HSIC','HEPA','HTBK','HFWA','HCCI','MLHR','HRTX','HSKA',
           'HX','HFFG','HIBB','SNLN','HIHO','HIMX','HIFS','HQI','HSTO','HCCH','HCCHR','HCCHU','HCCHW','HMNF',
           'HMSY','HOLI','HOLX','HBCP','HOMB','HFBL','HMST','HTBI','FIXX','HOFT','HOOK','HOPE','HBNC','HRZN',
           'HZNP','TWNK','TWNKW','HOTH','HMHC','HWCC','HOVNP','HBMD','HTGM','HTHT','HUBG','HUSN','HECCU','HSON',
           'HDSN','HUIZ','HBAN','HBANN','HBANO','HURC','HURN','HCM','HBP','HVBC','HYMC','HYMCW','HYRE','IIIV',
           'IAC','IBKC','IBKCN','IBKCO','IBKCP','IBEX','ICAD','IEP','ICCH','ICFI','ICHR','ICLK','ICLR','ICON',
           'ICUI','IPWR','IDEX','IDYA','INVE','IDRA','IDXX','IEC','IESC','IROQ','IFMK','IGMS','IHRT','INFO',
           'IIVI','IKNX','ILMN','IMAB','IMAC','IMACW','ISNS','IMRA','IMBI','IMMR','ICCC','IMUX','IMGN','IMMU',
           'IMVT','IMVTU','IMVTW','IMRN','IMRNW','IMMP','PI','IMV','NARI','INCY','INDB','IBCP','IBTX','ILPT',
           'INFN','INFI','IFRX','III','IEA','IEAWW','IMKTA','INMD','INMB','IPHA','INWK','INOD','IOSP','ISSC',
           'INVA','INGN','INOV','INO','INPX','INSG','NSIT','ISIG','INSM','INSE','IIIN','PODD','INSU','INSUU',
           'INSUW','NTEC','IART','IMTE','INTC','NTLA','IDN','IPAR','IBKR','ICPT','IDCC','TILE','IBOC','IGIC',
           'IGICW','IMXI','IDXG','XENT','IPLDP','IVAC','INTL','ITCI','IIN','INTU','ISRG','PLW','ADRE','BSCK',
           'BSJK','BSCL','BSJL','BSML','BSAE','BSCM','BSJM','BSMM','BSBE','BSCN','BSJN','BSMN','BSCE','BSCO',
           'BSJO','BSMO','BSDE','BSCP','BSJP','BSMP','BSCQ','BSJQ','BSMQ','BSCR','BSJR','BSMR','BSCS','BSMS',
           'BSCT','BSMT','PKW','PFM','PYZ','PEZ','PSL','PIZ','PIE','PXI','PFI','PTH','PRN','PDP','DWAS',
           'PTF','PUI','IDLB','PRFZ','PIO','PGJ','PEY','IPKW','PID','KBWB','KBWD','KBWY','KBWP','KBWR','PNQI',
           'PDBC','QQQ','ISDX','ISDS','ISEM','IUS','IUSS','USLB','PSCD','PSCC','PSCE','PSCF','PSCH','PSCI',
           'PSCT','PSCM','PSCU','VRIG','PHO','ISTR','CMFNL','ICMB','ISBC','ITIC','NVIV','IONS','IOVA','IPGP',
           'CLRG','CSML','IQ','IRMD','IRTC','IRIX','IRDM','IRBT','IRWD','IRCP','SLQD','ISHG','SHY','TLT',
           'IEI','IEF','AIA','USIG','COMT','ISTB','IXUS','IUSG','IUSV','IUSB','HEWG','SUSB','ESGD','ESGE',
           'LDEM','ESGU','SUSL','SUSC','XT','FALN','IFEU','IFGL','BGRN','IGF','GNMA','IBTA','IBTB','IBTD',
           'IBTE','IBTF','IBTG','IBTH','IBTI','IBTJ','HYXE','IGIB','IGOV','EMB','MBB','JKI','ACWX','ACWI',
           'AAXJ','EWZS','MCHI','SCZ','EEMA','EMXC','EUFN','IEUS','RING','SDG','EWJE','EWJV','ENZL','QAT',
           'TUR','UAE','IBB','SOXX','PFF','AMCA','EMIF','ICLN','WOOD','INDY','IJT','DVY','SHV','IGSB','ITMR',
           'ITI','ITRM','ITRI','ITRN','ISEE','IZEA','JJSF','MAYS','JBHT','JCOM','JKHY','JACK','JAGX','JAKK',
           'JRVR','JAN','JSML','JSMD','JAZZ','JD','JRSH','JBLU','JCTCF','JFIN','JMPNL','JMPNZ','JBSS','JOUT',
           'JNCE','YY','KALU','KXIN','KALA','KLDO','KALV','KMDA','KNDI','KRTX','KPTI','KZIA','KBLM','KBLMR',
           'KBLMU','KBLMW','KBSF','KRNY','KELYA','KELYB','KFFB','KROS','KEQU','KTCC','KZR','KFRC','KE','KBAL',
           'KIN','KGJI','KC','KINS','KNSA','KNSL','KIRK','KTOV','KTOVW','KLAC','KLXE','KOD','KOPN','KRNT',
           'KOSS','KWEB','KTOS','KRYS','KLIC','KURA','KRUS','KVHI','FSTR','LJPC','LSBK','LBAI','LKFN','LAKE',
           'LRCX','LAMR','LANC','LCA','LCAHU','LCAHW','LNDC','LARK','LMRK','LMRKN','LMRKO','LMRKP','LE',
           'LSTR','LTRN','LNTH','LTRX','LRMR','LSCC','LAUR','LAWS','LAZY','LCNB','LPTX','LEGH','LEGN','INFR',
           'LVHD','SQLV','LACQ','LACQU','LACQW','LMAT','TREE','LEVL','LXRX','LX','LFAC','LFACU','LFACW',
           'LGIH','LHCG','LLIT','LBRDA','LBRDK','LBTYA','LBTYB','LBTYK','LILA','LILAK','BATRA','BATRK','FWONA',
           'FWONK','LSXMA','LSXMB','LSXMK','LTRPA','LTRPB','LSAC','LSACU','LSACW','LCUT','LFVN','LWAY','LGND',
           'LTBR','LPTH','LLEX','LMB','LLNW','LMST','LMNL','LMNR','LINC','LECO','LIND','LPCN','LIQT','YVR',
           'LQDA','LQDT','LFUS','LIVK','LIVKU','LIVKW','LIVN','LOB','LIVE','LPSN','LIVX','LVGO','LIZI','LKQ',
           'LMFA','LMFAW','LMPX','LOGC','LOGI','LOGM','CNCR','CHNA','LONE','LOAC','LOACR','LOACU','LOACW',
           'LOOP','LORL','LPLA','LYTS','LK','LULU','LITE','LMNX','LUMO','LUNA','LKCO','LBC','LYFT','LYRA',
           'MCBC','MFNC','MTSI','MGNX','MDGL','MAGS','MGLN','MGTA','MGIC','MGYR','MHLD','MNSB','MJCO','MMYT',
           'MBUU','MLVF','TUSK','MANH','LOAN','MNTX','MTEX','MNKD','MANT','MARA','MCHX','MRIN','MARPS','MRNS',
           'MRKR','MKTX','MRLN','MAR','MBII','MRTN','MMLP','MRVL','MASI','MCFT','MTCH','MTLS','MTRX','MAT',
           'MATW','MXIM','MGRC','MDCA','MDJH','MDRR','MDRRP','MBNKP','MFIN','MFINL','MDIA','MNOV','MDGS','MDGSW',
           'MDWD','MEDP','MEIP','MGTX','MLCO','MNLO','MTSL','MELI','MBWM','MERC','MBIN','MBINO','MBINP','MFH',
           'MRCY','MREO','MCMJ','MCMJW','EBSB','VIVO','MRBK','MMSI','SNUG','MACK','MRSN','MRUS','MESA','MLAB',
           'MESO','CASH','METX','METXW','MEOH','MCBS','MGEE','MGPI','MBOT','MCHP','MU','MSFT','MSTR','MVIS',
           'MICT','MPB','MTP','MCEP','MBCN','MSEX','MSBI','MSVB','MOFG','MIST','MLND','TIGO','MIME','MNDO',
           'NERV','MGEN','MRTX','MIRM','MSON','MIND','MINDP','MITK','MKSI','MMAC','MTC','MINI','MOBL','MRNA',
           'MOGO','MWK','MKD','MTEM','MBRX','MNTA','MOMO','MKGI','MCRI','MDLZ','MGI','MDB','MNCL','MNCLU',
           'MNCLW','MPWR','MNPR','MNRO','MRCC','MRCCL','MNST','MORN','MORF','MOR','MOSY','MOTA','MPAA','MOTS',
           'MCACU','MOXC','COOP','MSBF','MTBC','MTBCP','MTSC','GRIL','MBIO','MVBF','MYSZ','MYL','MYOK','MYOS',
           'MYRG','MYGN','NBRV','NAKD','NNDM','NSTG','NAOV','NH','NK','NSSC','NDAQ','NTRA','NATH','NKSH','FIZZ',
           'NCMI','NESR','NESRW','NGHC','NGHCN','NGHCO','NGHCP','NGHCZ','NHLD','NHLDW','NATI','NRC','NSEC','EYE',
           'NWLI','NAII','NHTC','NATR','NTUS','JSM','NAVI','NMCI','NBTB','NCSM','NKTR','NMRD','NEOG','NEO','NLTX',
           'NEON','NEOS','NVCN','NEPH','NEPT','UEPS','NETE','NTAP','NTES','NFIN','NFINU','NFINW','NFLX','NTGR',
           'NTCT','NTWK','NBSE','NRBO','NBIX','NURO','STIM','NTRP','NBEV','NFE','NPA','NPAUU','NPAWW','NYMT',
           'NYMTM','NYMTN','NYMTO','NYMTP','NEWA','NBAC','NBACR','NBACU','NBACW','NWL','NWGI','NMRK','NWS','NWSA',
           'NEWT','NEWTI','NEWTL','NXMD','NXST','NXTC','NEXT','NXGN','NGM','NODK','EGOV','NICE','NICK','NCBS',
           'NKLA','NKLAW','NIU','LASR','NMIH','NNBR','NBL','NBLX','NDLS','NDSN','NSYS','NBN','NTIC','NTRS',
           'NTRSO','NFBK','NRIM','NWBI','NWPX','NLOK','NCLH','NWFL','NVFY','NVMI','NOVN','NOVT','NVAX','NVCR',
           'NOVS','NOVSU','NOVSW','NVUS','NUAN','NCNA','NTNX','NUVA','QQQX','NVEE','NVEC','NVDA','NXPI','NXTD',
           'NYMX','OIIM','OVLY','OCSL','OCSI','OMP','OAS','OBLN','OBSV','OBCI','OPTT','OCFC','OCFCP','OFED',
           'OCGN','OCUL','ODT','OMEX','ODP','OPI','OPINI','OFS','OFSSI','OFSSL','OFSSZ','OCCI','OCCIP','OVBC',
           'OKTA','ODFL','ONB','OPOF','OSBC','OLLI','ZEUS','OFLX','OMER','OMCL','ON','ONCY','ONTX','ONTXW','ONCS',
           'ONCT','OSS','OSPN','OSW','ONEW','OPBK','LPRO','OTEX','OPRA','OPES','OPESU','OPESW','OPGN','OPNT',
           'OPK','OPRT','OBAS','OCC','OPRX','OPHC','OPTN','OPCH','ORMP','OSUR','ORBC','OEG','ORTX','ORLY','OGI',
           'ORGO','ONVO','ORGS','ORIC','SEED','OBNK','OESX','ORSN','ORSNR','ORSNU','ORSNW','ORRF','OFIX','KIDS',
           'OSIS','OSMT','OSN','OTEL','OTG','OTIC','OTTW','OTTR','OTLK','OTLKW','OSTK','OVID','OXBR','OXBRW',
           'OXFD','OXLC','OXLCM','OXLCO','OXLCP','OXSQ','OXSQL','OXSQZ','OYST','PFIN','PTSI','PCAR','HERD','ECOW',
           'VETS','PACB','PEIX','PMBC','PPBI','PCRX','PACW','PAE','PAEWW','PLMR','PAAS','PANL','PZZA','PRTK',
           'TEUM','PCYG','PKBK','PKOH','PTNR','PASG','PBHC','PATK','PNBK','PATI','PDCO','PTEN','PAVM','PAVMW',
           'PAVMZ','PAYX','PCTY','PYPL','PAYS','CNXN','PCB','PCIM','PCSB','PCTI','PDCE','PDFS','PDLI','PDLB',
           'PDSB','PGC','PEER','PEGA','PTON','PENN','PVAC','PFLT','PNNT','PNNTG','PWOD','PEBO','PEBK','PFIS',
           'PBCT','PBCTP','PUB','PEP','PRCP','PRDO','PRFT','PSHG','PFMT','PERI','PESI','PPIH','PSNL','PETQ','PETS',
           'PFSW','PGTI','PHAS','PHAT','PAHC','PHIO','PHIOW','PLAB','PHUN','PHUNW','PICO','PLL','PIRS','PPC',
           'PDD','PME','PNFP','PNFPP','PT','PBFS','PPSI','PXLW','PLYA','PLXS','PLRX','PLUG','PLBC','PS','PSTI',
           'PSTV','PLXP','PCOM','POLA','PTE','PYPD','POOL','BPOP','BPOPM','BPOPN','KCAPL','PTMN','PTLA','PPHI',
           'PBPB','PCH','POWL','POWI','PBTS','PWFL','PPD','PRAA','PRAH','PGEN','PRPO','DTIL','POAI','PFBC',
           'PLPC','PFBI','PINC','PBIO','PRVL','PRGX','PSMT','PNRG','PRMW','PRIM','PVAL','PFG','BTEC','PDEV',
           'GENY','PSET','PY','PMOM','PLC','USMC','PSC','PSM','PRNB','PRTH','UFO','PDEX','IPDN','PFHD','PAAC',
           'PAACR','PAACU','PAACW','PFIE','PROF','PGNX','PRGS','PGNY','LUNG','PFPT','PRPH','PTAC','PTACU','PTACW',
           'PRQR','EQRR','BIB','TQQQ','SQQQ','BIS','PSEC','PTGX','TARA','PTVCA','PTVCB','PTI','PRTA','PRVB',
           'PVBC','PROV','PBIP','PMD','PTC','PTCT','PHCF','PULM','PLSE','PBYI','PACQ','PACQU','PACQW','PCYO',
           'PRPL','PUYI','PXS','QK','QADA','QADB','QCRH','QGEN','QIWI','QRVO','QCOM','QLGN','QLYS','QTRX','QMCO',
           'QRHC','QUIK','QDEL','QNST','QUMU','QTNT','QRTEA','QRTEB','QTT','RRD','RCM','RADA','RDCM','RDUS',
           'RDNT','RDWR','METC','RMBS','RAND','RNDB','RPD','RAPT','RTLR','RAVE','RAVN','RBB','ROLL','RICK','RCMT',
           'RDI','RDIB','BLCN','RNWK','RP','RETA','RCON','REPH','RRBI','RRGB','RRR','RDVT','RDFN','RDHL','REED',
           'REG','REGN','RGNX','RGLS','REKR','RBNC','RELV','RLMD','MARK','RNST','REGI','RCII','RPAY','RGEN',
           'REPL','KRMD','RBCAA','FRBK','REFR','RSSS','RESN','RGP','TORC','ROIC','RETO','RTRX','RVNC','RVMD',
           'RWLK','REXN','REYN','RFIL','RGCO','RBKB','RYTM','RBBN','RIBT','RELL','RMBI','RIGL','RNET','RMNI',
           'RIOT','REDU','RVSB','RIVE','RCKT','RMTI','RCKY','RMCF','ROKU','ROSE','ROSEU','ROSEW','ROST','ROCH',
           'ROCHU','ROCHW','RGLD','RTIX','RBCN','RUBY','RUHN','RMBL','RUSHA','RUSHB','RUTH','RYAAY','STBA',
           'SANW','SBRA','SABR','SAEX','SFET','SAFT','SGA','SAGE','SAIA','SLRX','SALM','SAL','SAFM','SASR',
           'SGMO','SANM','SNY','SPNS','SRPT','STSA','SVRA','SBFG','SBBX','SBAC','SCSC','SMIT','SCHN','SRRK',
           'SCHL','SDGR','SAMA','SAMAU','SAMAW','SJ','SGMS','SCPL','SCPH','WORX','SCYX','SEAC','SBCF','STX',
           'SHIP','SHIPW','SHIPZ','SPNE','SGEN','EYES','EYESW','SECO','SCWX','SNFCA','SEEL','SEIC','SLCT','SIC',
           'SELB','SIGI','SLS','LEDS','SMTC','SNCA','SENEA','SENEB','SNES','AIHS','SRTS','SQBG','MCRB','SVC',
           'SREV','SFBS','SESN','SVBI','SGBX','SGOC','SMED','SHSP','SHEN','PIXY','SHLO','SCCI','TYHT','SWAV',
           'SCVL','SHBI','SSTI','SIBN','SIEB','SIEN','BSRR','SRRA','SWIR','SIFY','SIGA','SGLB','SGLBW','SGMA',
           'SBNY','SLGN','SILC','SLAB','SIMO','SILK','SSPK','SSPKU','SSPKW','SAMG','SSNT','SFNC','SLP','SINA',
           'SBGI','SINO','SVA','SINT','SG','SIRI','SRVA','SITM','SKYS','SKYW','SWKS','SNBR','SLM','SLMBP','SGH',
           'SND','SMBK','SDC','SWBI','SMSI','SMTX','SCKT','GIGE','SAQN','SAQNU','SAQNW','SOHU','SLRC','SUNS',
           'SEDG','SLNO','SLGL','SLDB','SNGX','SNGXW','SOLY','SONM','SONN','SNOA','SONO','SRNE','SOHO','SOHOB',
           'SOHON','SOHOO','SFBC','SMMC','SMMCU','SMMCW','SPFI','SSB','SFST','SMBC','SONA','SBSI','SY','SP',
           'SGRP','SPKE','SPKEP','SPTN','DWFI','SPPI','SPRO','ANY','SPI','SAVE','STXB','SPLK','SPOK','SPWH',
           'SBPH','SWTX','FUND','SPT','SFM','SPSC','SRAX','SSNC','SSRM','STAA','SRAC','SRACU','SRACW','STAF',
           'STMP','STND','SBLK','SBLKZ','SBUX','STFC','MITO','GASS','STCN','STLD','SMRT','SRCL','SBT','STRL',
           'SHOO','SFIX','SYBT','STOK','BANX','STNE','SSKN','SSYS','STRA','HNDL','STRT','STRS','STRM','SBBP',
           'SUMR','SMMF','SSBI','SMMT','WISA','SNDE','SNDL','SNSS','STKL','SPWR','RUN','SUNW','SLGG','SMCI',
           'SPCB','SCON','SGC','SUPN','SPRT','SURF','SGRY','SRDX','STRO','SSSS','SIVB','SIVBP','SVMK','SWKH',
           'SYKE','SYNC','SYNL','SYNA','SNCR','SNDX','SYNH','SYBX','SNPS','SYPR','SYRS','TROW','TTOO','TRHC',
           'TCMD','TAIT','TLC','TTWO','TLND','TNDM','TLF','TANH','TAOP','TAPM','TEDU','TH','THWWW','TATT','TAYD',
           'TCF','TCFCP','CGBD','TCRR','AMTD','GLG','PETZ','TECD','TCCO','TTGT','TGLS','TGEN','TECTP','TELA',
           'TNAV','TLGT','TELL','TENB','TENX','TZAC','TZACU','TZACW','TER','TERP','TBNK','TSLA','TESS','TTEK',
           'TTPH','TCBI','TCBIL','TCBIP','TXN','TXRH','TFFP','TFSL','TGTX','WTER','ANDE','TBBK','BPRN','CG',
           'CAKE','CHEF','TCFC','DSGX','DXYN','ENSG','XONE','FBMS','FLIC','GT','HCKT','HAIN','CUBA','INTG','JYNT',
           'KHC','OLD','LOVE','MEET','MIK','MIDD','STKS','PECK','PNTG','PRSC','REAL','RMR','RUBI','SHYF','SMPL',
           'TTD','YORW','NCTY','TXMD','TRPX','THTX','TBPH','THMO','TCRD','THBR','THBRU','THBRW','TLRY','TSBK',
           'TIPT','TITN','TMDI','TTNP','TVTY','TLSA','TMUS','TOCA','TNXP','TOPS','TRCH','TRMD','TOTA','TOTAR',
           'TOTAU','TOTAW','TBLT','TBLTW','TSEM','CLUB','TOWN','TPIC','TCON','TSCO','TW','TWMC','TACT','TRNS',
           'TGA','TBIO','TMDX','TA','TANNI','TANNL','TANNZ','TZOO','TRMT','TRVN','TRVI','TPCO','TCDA','TCBK',
           'TDAC','TDACU','TDACW','TRIL','TRS','TRMB','TRIB','TCOM','TRIP','TSC','TSCAP','TSCBP','TBK','TRVG',
           'TRUE','TRUP','TRST','TRMK','MEDS','TSRI','TTEC','TTMI','TC','TCX','TOUR','TPTX','HEAR','THCB','THCBU',
           'THCBW','THCA','THCAU','THCAW','TWIN','TWST','TYME','USCR','PRTS','USEG','GROW','USAU','USWS','USWSW',
           'UCL','UFPI','UFPT','ULTA','UCTT','RARE','ULBI','UMBF','UMPQ','UNAM','LATN','LATNU','LATNW','UNB',
           'QURE','UAL','UBCP','UBOH','UBSI','UCBI','UCBIO','UFCS','UIHC','UNFI','UBFO','USLM','UTHR','UG','UNIT',
           'UNTY','UBX','OLED','UEIC','ULH','USAP','UVSP','UMRX','TTTN','TIGR','UPLD','UPWK','UONE','UONEK','URBN',
           'MYT','URGN','UROV','ECOL','ECOLW','USAK','USIO','UTMD','UTSI','UXIN','VCNX','VLY','VLYPO','VLYPP',
           'VTEC','VALU','VNDA','BBH','ANGL','BJK','PPH','RTH','SMH','ESPO','VWOB','VNQI','VCIT','VGIT','VIGI',
           'VYMI','VCLT','VGLT','VMBS','VONE','VONG','VONV','VTWO','VTWG','VTWV','VTHR','VCSH','VTIP','VGSH','BND',
           'VTC','BNDX','VXUS','BNDW','VREX','VRNS','VBLT','VXRT','PCVX','VBIV','VECO','VERO','VEON','VRA',
           'VCYT','VSTM','VERB','VERBW','VCEL','VERY','VRNT','VRSN','VRSK','VBTX','VERI','VRNA','VRRM','VRCA',
           'VTNR','VRTX','VERU','VIAC','VIACA','VSAT','VIAV','VICR','VCTR','CIZ','VSDA','CEY','CEZ','CID','CIL',
           'CFO','CFA','CSF','CDC','CDL','VSMV','CSB','CSA','VIE','VMD','VRAY','VKTX','VKTXW','VBFC','VFF',
           'VLGEA','VIOT','VNOM','VIR','VIRC','VTUS','VTSI','VIRT','VRTS','BBC','BBP','VRTU','VISL','VTGN','VC',
           'VIVE','VVPR','VVUS','VOD','VG','VOXX','VYGR','VRM','VSEC','VTVT','VUZI','WAFU','HLAL','WTRH','WBA',
           'WSG','WMG','WAFD','WASH','WSBF','WTRE','WTREP','WVE','WNFM','WSTG','WDFC','WB','WEN','WERN','WSBC',
           'WTBA','WABC','WSTL','WINC','WBND','WDC','WNEB','WPRT','WWR','WEYS','WHLR','WHLRD','WHLRP','WHF',
           'WHFBZ','WHLM','WVVI','WVVIP','WLDN','WLFC','WLTW','WSC','WIMI','WINT','WING','WINA','WINS','WTFC',
           'WTFCM','WTFCP','CXSE','WCLD','EMCB','DGRE','DXGE','HYZD','AGZD','WETF','DXJS','DGRW','DGRS','WKEY',
           'WIX','WWD','WDAY','WKHS','WRLD','WRTC','WMGI','WSFS','WVFC','WW','WYNN','XFOR','XBIT','XELB','XEL',
           'XNCR','XBIO','XBIOW','XENE','XERS','XLNX','XOMA','XP','XPEL','XPER','XSPA','XTLB','XNET','YNDX',
           'YTRA','YTEN','YIN','YMAB','YGYI','YGYIP','YRCW','CTIB','ZGYH','ZGYHR','ZGYHU','ZGYHW','YJ','ZAGG',
           'ZLAB','ZEAL','ZBRA','ZNTL','ZCMD','Z','ZG','ZN','ZNWAA','ZION','ZIONL','ZIONN','ZIONO','ZIONP',
           'ZIOP','ZIXI','ZKIN','ZGNX','ZM','ZI','ZSAN','ZVO','ZS','ZUMZ','ZYNE','ZYXI','ZNGA']


NASDAQ = chunks(list(nasdaq.nasdaq_tickers), 4)
AMEX = chunks(list(amex.amex_tickers), 4)
NYSE = chunks(list(nyse.nyse_tickers), 4)