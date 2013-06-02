var babyCharter=function(targ1,targ2,targ3,request,yearDist){

	this.yearTotals=yearDist;

	var tempData;

	this.targ1=targ1;
	this.targ2=targ2;
	this.targ3=targ3;
};

babyCharter.prototype.initChart2=function(info){
	console.log("We are here");

	this.data=info;

	this.graphSex=[true,true];

	this.ageLabels=[];

	for(var i=1;i<=69;i++){
		this.ageLabels.push(i.toString());
	}

	this.yearLabels=[];

	for(var i=1944;i<=2012;i++){
		this.yearLabels.push(i.toString());
	}

	this.yearGraphSeries=[];

	this.ageGraphSeries=[];

	this.rankGraphSeries=[];

	for(var a in info){
		this.yearGraphSeries.push({
			id:a+'_males',
			name:'Men',
			color:'#32abf7',
			data:info[a]['males']['years']
		});

		this.yearGraphSeries.push({
			id:a+'_females',
			name:'Women',
			color:'#f74978',
			data:info[a]['females']['years']
		});

		this.rankGraphSeries.push({
			id:a+'_males',
			name:'Men',
			color:'#32abf7',
			data:info[a]['males']['ranks']
		});

		this.rankGraphSeries.push({
			id:a+'_females',
			name:'Women',
			color:'#f74978',
			data:info[a]['females']['ranks']
		});

		this.ageGraphSeries.push({
			id:a+"_males",
			name:'Men',
			color:'#32abf7',
			data:info[a]['males']['ages']
		});

		this.ageGraphSeries.push({
			id:a+"_females",
			name:'Women',
			color:'#f74978',
			data:info[a]['females']['ages']
		});
	}

	// for(var i=0, len=this.yearGraphSeries.length;i<len;i++){
	// 	this.yearGraphSeries[i]=this.yearsIntoProp(10000,this.yearGraphSeries[i]);
	// }


	this.yearChart=new Highcharts.Chart({
		chart:{
			renderTo:this.targ1,
			type:'area'
		},
		title:{
			text:'Yearly Distribution'
		},
		xAxis:{
			categories:this.yearLabels,
			labels:{
				rotation:90,
				style:{
					fontSize:'8px'
				}
			}
		},
		yAxis:{
			min:0,
			title:{
				text:"Babies"
			}
		},
		series:this.yearGraphSeries
	});

	this.rankChart=new Highcharts.Chart({
		chart:{
			renderTo:this.targ3,
			type:'area'
		},
		title:{
			text:'Rank per Year'
		},
		xAxis:{
			categories: this.yearLabels,
			labels:{
				rotation:90,
				style:{
					fontSize:'8px'
				}
			}
		},
		yAxis:{
			min:0,
			title:{
				text:"Rank"
			}
		},
		series:this.rankGraphSeries
	});

	this.ageChart=new Highcharts.Chart({
		chart:{
			renderTo:this.targ2,
			type:'area'
		},
		title:{
			text:'Age Distribution'
		},
		xAxis:{
			categories:this.ageLabels,
			labels:{
				rotation:90,
				style:{
					fontSize:'8px'
				}
			}
		},
		yAxis:{
			min:0,
			title:{
				text:"Percentage Aged..."
			}
		},
		series:this.ageGraphSeries
	});

	console.log(this.yearChart);
}

babyCharter.prototype.yearsIntoProp=function(propof,yearseries){
	var thisholder=this;
	if(yearseries['id'].substr(-8)=='_females'){
		yearseries['data']=$.map(yearseries['data'],function(ele,ind){
			return Math.round(propof*ele/thisholder.yearTotals['females'][ind]*100);
		});
	}
	else{
		yearseries['data']=$.map(yearseries['data'],function(ele,ind){
			return Math.round(propof*ele/thisholder.yearTotals['males'][ind]*100);
		});
	}

	console.log(yearseries);

	return yearseries;
}

babyCharter.prototype.initChart=function(name){

	var thisholder=this;

	$.getJSON('http://127.0.0.1:8000/babynames/namejson/'+name+'/',function(data){
		thisholder.initChart2(data);
	});
}

babyCharter.prototype.hasSeries=function(seriesname){
	// Checks to see if a series already exists on the chart
	var remainArr=$.grep(this.yearGraphSeries,function(ele,ind){
		return ele.id==seriesname+'_males';
	});

	console.log(remainArr);

	return remainArr.length!=0;
}

babyCharter.prototype.addSeries=function(info){
	// Make sure that you don't already have each

	var newAgeSeries=[];
	var newYearSeries=[];
	var newRankSeries=[];

	var tempSeries={};

	for(var a in info){
		if(this.hasSeries(a)){
			continue;
		}

		tempSeries={
			id:a+'_males',
			name:a,
			data:info[a]['males']['years']
		};

		// tempSeries=this.yearsIntoProp(10000,tempSeries);

		this.yearGraphSeries.push(tempSeries);

		newYearSeries.push(tempSeries);

		tempSeries={
			id:a+'_females',
			name:a,
			data:info[a]['females']['years']
		};

		// tempSeries=this.yearsIntoProp(10000,tempSeries);

		this.yearGraphSeries.push(tempSeries);

		newYearSeries.push(tempSeries);

		tempSeries={
			id:a+'_males',
			name:a,
			data:info[a]['males']['ranks']
		};

		// tempSeries=this.yearsIntoProp(10000,tempSeries);

		this.rankGraphSeries.push(tempSeries);

		newRankSeries.push(tempSeries);

		tempSeries={
			id:a+'_females',
			name:a,
			data:info[a]['females']['ranks']
		};

		// tempSeries=this.yearsIntoProp(10000,tempSeries);

		this.rankGraphSeries.push(tempSeries);

		newRankSeries.push(tempSeries);

		tempSeries={
			id:a+"_males",
			name:a,
			data:info[a]['males']['ages']
		};

		this.ageGraphSeries.push(tempSeries);

		newAgeSeries.push(tempSeries);

		tempSeries={
			id:a+"_females",
			name:a,
			data:info[a]['females']['ages']
		};

		this.ageGraphSeries.push(tempSeries);

		newAgeSeries.push(tempSeries);
	}

	// Now add all these bad-boys to the graph
	for(var i=0, len=newAgeSeries.length;i<len;i++){
		this.ageChart.addSeries(newAgeSeries[i],false);
		this.yearChart.addSeries(newYearSeries[i],false);
		this.rankChart.addSeries(newRankSeries[i],false);
	}

	this.ageChart.redraw();
	this.yearChart.redraw();
	this.rankChart.redraw();
}

babyCharter.prototype.removeSeries=function(idArr){
	// Make sure you DO have each
	for(var i=0, len=idArr.length;i<len;i++){
		if(this.hasSeries(idArr[i])){
			this.ageChart.get(idArr[i]+'_males').remove(false);
			this.ageChart.get(idArr[i]+'_females').remove(false);
			this.yearChart.get(idArr[i]+'_males').remove(false);
			this.yearChart.get(idArr[i]+'_females').remove(false);
			this.rankChart.get(idArr[i]+'_males').remove(false);
			this.rankChart.get(idArr[i]+'_females').remove(false);

			this.ageGraphSeries=$.grep(this.ageGraphSeries,function(ele,ind){
				return ele.id!=idArr[i]+'_males'&&ele.id!=idArr[i]+'_females';
			});

			this.yearGraphSeries=$.grep(this.yearGraphSeries,function(ele,ind){
				return ele.id!=idArr[i]+'_males'&&ele.id!=idArr[i]+'_females';
			});

			this.rankGraphSeries=$.grep(this.rankGraphSeries,function(ele,ind){
				return ele.id!=idArr[i]+'_males'&&ele.id!=idArr[i]+'_females';
			});
		}
	}

	this.ageChart.redraw();
	this.yearChart.redraw();
}