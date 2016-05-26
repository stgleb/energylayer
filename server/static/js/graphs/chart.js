
var data = [];
var mode = 'Live Stats';
var monthes = ['January','February','March','April','May','June','July','August','September','October','November','December'];
var temperature = [];
var totalPoints = 180; //The total memory is 180 sec (3 min)
//var totalPoints = 10800; //The total memory is 60 min
var updateInterval = 1000; // 200 x 1000 = 200sec (3min)
//var updateInterval = 20000; //(30 min)
var now = new Date().getTime() - totalPoints * updateInterval; //200 x 1000


function GetData() {
	data.shift();
	temperature.shift();

	// do a random walk
	// for power chart
	while (data.length < totalPoints) {
	    var tempDelta;
		var prev = data.length > 0 ? data[data.length - 1] : [now, 50];
		//var prev = data.length > 0 ? data[0] : [now, 50];
		//console.log("data[data.length - 1]: ", data[data.length - 1]);
		var y = prev[1] + Math.random() * 10 - 5; // for 200 total points
		//var y = prev[1] + Math.random() - 0.5; // for 10800 (3 hour) total points
		//console.log("y: ", y);
		if (y < 15)
			y = 15;
		if (y > 80)
			y = 80;
		//var temp = [now += updateInterval, y];
		var temp = [now += updateInterval, y];
        data.push(temp);

		/*
		//for temperature
	    var prev1 = temperature.length > 0 ? temperature[temperature.length - 1] : [now, 50];
		var z = prev1[1] + Math.random() * 10 - 5;
		if (z < 15)
			z = 15;
		if (z > 80)
			z = 80;
		var temp1 = [now += updateInterval, z];
        temperature.push(temp1);
		*/
	}
   	//now = new Date().getTime();
	firstTime = 0;
}

var options;
function initOptions(){
	var tick;
	//tick = [0.03 * updateInterval, "second"];
	//if (mode == 'Week')
		tick: [2, "day"];
	options = {
		series: {
			lines: {
				show: true,
				lineWidth: 2,
				fill: true,
				fillColor: { colors: [ { opacity: 0.4 }, { opacity: 0 } ] },
			}
		},
		xaxis: {
			mode: "time",
			//tickSize: [30, "second"],
			//tickSize: [totalPoints/10, "second"],
			//tickSize: [0.03 * updateInterval, "second"],
			tickSize: tick,

			tickFormatter: function (v, axis) {
				var date = new Date(v);
				//if (date.getSeconds() % 60 == 0) {
				//if (date.getSeconds() % totalPoints/10 == 0) {
				if (date.getSeconds() % 0.06 * updateInterval == 0) {
				    var month = monthes[date.getUTCMonth() + 1]; //months from 1-12
					var day = date.getUTCDate();
					var newdate = month + "/" + day;

					var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
					var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
					var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
					if (mode == 'Week')
						return newdate + ", " + hours + ":" + minutes;
					return hours + ":" + minutes + ":" + seconds;
				}
				else {
					return "";
				}
			},
			axisLabel: "Time",
			axisLabelUseCanvas: true,
			axisLabelFontSizePixels: 12,
			axisLabelFontFamily: 'Verdana, Arial',
			axisLabelPadding: 10
		},
		yaxis: {
			min: 0,
			max: 100,
			tickSize: 20,
			tickFormatter: function (v, axis) {
				if (v % 10 == 0) {
					return v + " watt";
				} else {
					return "";
				}
			},
			axisLabel: "Energy generated",
			axisLabelUseCanvas: true,
			axisLabelFontSizePixels: 12,
			axisLabelFontFamily: 'Verdana, Arial',
			axisLabelPadding: 6
		},
		legend: {
			labelBoxBorderColor: "#fff"
		},
		grid: {
			//backgroundColor: "#000000",
			backgroundColor: "#fff",
			//tickColor: "#008040"
			borderWidth: 1,
			hoverable: true, clickable: true, autoHighlight: true
		}
	};
}

$(document).ready(function () {
    GetData();

    dataset = [
        //{ label: "CPU", data: data, color: "#00FF00" }
		{ data: data, label: 'Energy generated', color: 'green' , points: { show: false }},
		//{ data: temperature, label: 'Temperature', color: '#ed7a53' , points: { show: false }}
    ];
	initOptions();
    $.plot($("#flot-placeholder1"), dataset, options);
	console.log('totalPoints * updateInterval: ', totalPoints * updateInterval);
	$("#flot-placeholder1").bind("plothover", function (event, pos, item) {

	/*  Tooltips  */

	/* 1. Adding tooltip */
	$("<div id='tooltip'></div>").css({
		position: "absolute",
		display: "none",
		border: "1px solid #fdd",
		padding: "2px",
		//"background-color": "#fee",
		"background-color": " #fff59d ",
		opacity: 0.80
	}).appendTo("body");

	/* 2. Put data in tooltip */
	if(item){
		//console.log('item: ', item.datapoint[1]);
		var dateTip = new Date(item.datapoint[0]);
		function pad(n){return n < 10 ? '0' + n : n} // for adding leading zeros
		dateTip = pad(dateTip.getHours()) + ":" + pad(dateTip.getMinutes()) + ":" + pad(dateTip.getSeconds());
		if (mode == 'Week')
			dateTip = pad(dateTip.getHours()) + ":" + pad(dateTip.getMinutes()) + ":" + pad(dateTip.getSeconds());
		$("#tooltip").html("<b>" + Math.floor(item.datapoint[1]) + " Watt </b> <br>" +  " <small>" + dateTip + " </small>")
		.css({top: item.pageY - 65, left: item.pageX - 10})
		.fadeIn(200);
		}
	 else{
			$("#tooltip").hide();
		}
	});

	var timerId
    function update() {
	console.log("update! ")
	    now = new Date().getTime();
        GetData();
        $.plot($("#flot-placeholder1"), dataset, options)
        timerId = setTimeout(update, updateInterval);
    }

    update();

	/* Manage tabs events*/
	var anchor;
	$( 'a[data-toggle="tab"]' ).on( 'shown.bs.tab', function( e ) {

		// Read the a text of the anchor that was clicked
		mode = $( e.target).context.innerText;

		console.log("text: ", mode)
		console.log("old updateInterval: ", updateInterval)

		/* Change update interval */
		switch (mode) {
			case 'Live Stats':
				updateInterval = 1000             //1 sec  / 3 minutes
				break
			case 'Hour':
				updateInterval = 20 * 1000        //20 sec  / 1 hour
				break
			case 'Day':
				updateInterval = 24 * 20 * 1000    //8 min   / 24 hours
				break
			case 'Week':
				updateInterval = 7 * 24 * 20 * 1000 //56 min / 7 days
				break
			default:
				alert('Я таких значений не знаю')
		}
		console.log("updateInterval: ", updateInterval);

		/* drop the data[] and run update */
		data=[]
		now = new Date().getTime() - totalPoints * updateInterval; //200 x 1000
		GetData();

		dataset = [
			//{ label: "CPU", data: data, color: "#00FF00" }
			{ data: data, label: 'Energy generated', color: 'green' , points: { show: false }},
			//{ data: temperature, label: 'Temperature', color: '#ed7a53' , points: { show: false }}
		];

		initOptions();

		$.plot($("#flot-placeholder1"), dataset, options);
			console.log('totalPoints * updateInterval: ', totalPoints * updateInterval)
		clearTimeout(timerId);
		update();

	});

});