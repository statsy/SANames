

#newdata<-read.table(file=paste("baby-names-1944-2012/",sex,"_cy",i,"_top.csv",sep=""),sep=",",header=T)
#newdata[is.na(newdata$Given.Name),]

#sex="male"
#i=1944

#sex="male"
#i=1973
#newdata[1091:1093,]

count=0
x<-data.frame()
for (i in c(1944:2005,2007:2012)) {
  for (sex in c("female","male")) {
    newdata<-read.table(file=paste("baby-names-1944-2012/",sex,"_cy",i,"_top.csv",sep=""),sep=",",header=T,na.strings="",stringsAsFactors=F)
    newdata$sex<-sex
    newdata$year<-i
    newdata$Position<-gsub("=","",newdata$Position)
    #Fixing duplicates in datasets. Eg John in 1944
    newdata<-newdata[with(newdata, order(Given.Name)), ]
    dups<-which(duplicated(newdata$Given.Name))
    len<-length(dups)
    len2<-len-1
    if (len>0) {
      if (len>1) {
      for (j in 1:len2) {
        if (dups[j]==dups[j+1]-1) {
          count<-count+1
          #print(i)
          #print(sex)
          #print(dups)
          newdata$Amount[dups[j]]<-newdata$Amount[dups[j]]+newdata$Amount[dups[j]+1]
        }}}
      for (j in 1:len) {
        newdata$Amount[dups[j]-1]<-newdata$Amount[dups[j]-1]+newdata$Amount[dups[j]]
      }   
      newdata<-newdata[-dups,]
    }
    newdata$Position<-rank(-newdata$Amount,ties.method="min")
    newdata<-newdata[with(newdata, order(-Amount,Given.Name)), ]
    
    newdata$Pop<-sum(newdata$Amount)
    newdata$Freq<-newdata$Amount/newdata$Pop
    x<-rbind(newdata,x)
  }
}

#write.table(x,file="babynames4.csv",col.names=T,row.names=T)

#Estimated age distribution at the start of 2013 of south australian born people

#Age-specific mortality rates for SA from ABS data
mortmale<-c(2.5,rep(0.2,4),rep(0.1,5),rep(0.1,5),rep(0.4,5),rep(0.6,5),rep(0.9,5),rep(1.1,5),rep(1.4,5),rep(1.8,5)
            ,rep(2.3,5),rep(3.9,5),rep(5.6,5),rep(8.4,5),rep(11.9,4))

mortfemale<-c(2.8,rep(0.2,4),rep(0.1,5),rep(0.1,5),rep(0.3,5),rep(0.2,5),rep(0.3,5),rep(0.5,5),rep(0.6,5),rep(0.9,5)
              ,rep(1.3,5),rep(2.2,5),rep(3.0,5),rep(4.8,5),rep(6.9,4))

cmortmale<-rep(1,70)
cmortfemale<-rep(1,70)

for (j in 1:69) {
  cmortmale[j+1]<-(1-mortmale[j]/1000)*cmortmale[j]
}
cmortmale<-cmortmale[-1]
for (j in 1:69) {
  cmortfemale[j+1]<-(1-mortfemale[j]/1000)*cmortfemale[j]
}
cmortfemale<-cmortfemale[-1]


#x$age<-2013-x$year


count=0
x<-data.frame()
for (i in c(1944:2005,2007:2012)) {
  for (sex in c("female","male")) {
    newdata<-read.table(file=paste("baby-names-1944-2012/",sex,"_cy",i,"_top.csv",sep=""),sep=",",header=T,na.strings="",stringsAsFactors=F)
    newdata$Given.Name<-gsub("","",newdata$Given.Name)
    newdata$sex<-sex
    newdata$year<-i
    newdata$age<-2013-i
    if (sex=="male") {
      newdata$mortfactor <- cmortmale[2013-i]
    }
    if (sex=="female") {
      newdata$mortfactor <- cmortfemale[2013-i]
    }
    
    newdata$Position<-gsub("=","",newdata$Position)
    #Fixing duplicates in datasets. Eg John in 1944
    newdata<-newdata[with(newdata, order(Given.Name)), ]
    dups<-which(duplicated(newdata$Given.Name))
    len<-length(dups)
    len2<-len-1
    if (len>0) {
      if (len>1) {
        for (j in 1:len2) {
          if (dups[j]==dups[j+1]-1) {
            count<-count+1
            #print(i)
            #print(sex)
            #print(dups)
            newdata$Amount[dups[j]]<-newdata$Amount[dups[j]]+newdata$Amount[dups[j]+1]
          }}}
      for (j in 1:len) {
        newdata$Amount[dups[j]-1]<-newdata$Amount[dups[j]-1]+newdata$Amount[dups[j]]
      }   
      newdata<-newdata[-dups,]
    }
    newdata$Position<-rank(-newdata$Amount,ties.method="min")
    newdata<-newdata[with(newdata, order(-Amount,Given.Name)), ]
    
    newdata$Pop<-sum(newdata$Amount)
    newdata$Freq<-newdata$Amount/newdata$Pop
    x<-rbind(newdata,x)
  }
}

x$AmountMort<-x$Amount*x$mortfactor

summed<-aggregate(AmountMort ~ Given.Name + sex,  sum, data = x)
names(summed)[3] <- "totalamountmort"

total <- merge(x,summed,by=c("Given.Name","sex"))
x2<-total[with(total, order(age,-Amount)), ]

x2$nameprop<-x2$AmountMort/x2$totalamountmort


#freqs<-x2$nameprop[x2$Given.Name=="JOHN" & x2$sex=="male"]
#ages<-x2$age[x2$Given.Name=="JOHN" & x2$sex=="male"]
#plot(ages,freqs)

#freqs<-x2$nameprop[x2$Given.Name=="SHANNON" & x2$sex=="female"]
#ages<-x2$age[x2$Given.Name=="SHANNON" & x2$sex=="female"]
#plot(ages,freqs)

new<-x2
new<-new[,-c(3,4,5,7,8,9)]
write.table(new,file="babynamesmortality2.csv",col.names=T,row.names=T)

