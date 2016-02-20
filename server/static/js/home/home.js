;
$(function () {
    var contextPath = $('#contextPath').data('contextpath');
    var chartContainer = $('#chart-placeholder');
    var totalPoints = 1300;
    var data = [];
    var sensorData = 100;
    var realTimeTimeout;
    var plot;
    var updateCount = 0;

    (function init(){
        initUI();
        bingEvents();
    })();
    function initUI(){
        loadDevices();
        initChart();
    }
    function bingEvents(){
        $('#realTime').on('click', function(){
            var $this = $(this);
            if ($this.hasClass('active')){
                return;
            }
            $this.addClass('active');
            $('#hourly').removeClass('active');
            $('#daily').removeClass('active');
            initChart();
        });
        $('#hourly').on('click', function(){
            var $this = $(this);
            if ($this.hasClass('active')){
                return;
            }
            $this.addClass('active');
            $('#realTime').removeClass('active');
            $('#daily').removeClass('active');
            drawHourly();
        });
        $('#daily').on('click', function(){
            var $this = $(this);
            if ($this.hasClass('active')){
                return;
            }
            $this.addClass('active');
            $('#realTime').removeClass('active');
            $('#hourly').removeClass('active');
            drawDaily();
        });
        $('#addDevice').on('click', function(){
            $('#devideDialog').dialog('open');
        });
        $('#devideDialog').dialog({
            autoOpen: false,
            title: "Add new device",
            buttons: [{
                text: "Add",
                click: function () {
                    var url = contextPath + '/device';
                    $("#deviceForm").ajaxSubmit({
                        url: url,
                        type: 'post',
                        success: function(){
                            drawDevice($('input[name=deviceId]').val(), 'device');
                            $('#devideDialog').dialog('close');
                        },
                        error: function(response){
                            $('#addDeviceResponseError').remove();
                            $('#deviceForm').after($('<span/>', {id:'addDeviceResponseError',text:response.responseText}));
                        }
                    })
                }
            }]
        });
        $('.device').on('click', function() {
            $('.device').removeClass('device-highlighted');
            $(this).addClass('device-highlighted');
        });
        $('.logout-btn').on('click', function() {
            $('.logout-form').submit();
        });
    }
    function loadDevices() {
        if($('.logged-in').length == 0) {
            drawDevices([1]);
            return;
        }
        $.ajax({
            url: contextPath + '/device/deviceIds',
            dataType: 'json',
            async: false,
            success: function (response) {
                if (response.length > 0) {
                    drawDevices(response);
                } else {
                    drawDevices([1]);
                }
            }
        });
    }
    function drawDevices(deviceIds) {
        $.each(deviceIds, function(i, val) {
            var style = 'device';
            if (i==0){
                style += ' device-highlighted';
            }
            drawDevice(val, style)
        });
    }
    function drawDevice(deviceId, style) {
        $('#deviceContainer').append($('<div/>', {text:deviceId,class:style}));
    }
    function drawDaily(){
        clearTimeout(realTimeTimeout);
        var deviceId = $('.device-highlighted').text();
        var sensorNumber = $('input[name=sensorNumber]').val();
        $.ajax({
            url: contextPath + '/rs/data/get/aggregated/' + deviceId + '/day?sensorNumber=' + sensorNumber,
            dataType: "json",
            success: function(response){
                plot = $.plot($(chartContainer), [{color: 'green', data: mapData(response.data)}], {
                    series: {
                        lines: {show: true, fill: 0.15, lineWidth: 4}
                    }
                });
            }
        });
    }
    function drawHourly(){
        clearTimeout(realTimeTimeout);
        var deviceId = $('.device-highlighted').text();
        var sensorNumber = $('input[name=sensorNumber]').val();
        $.ajax({
            url: contextPath + '/rs/data/get/aggregated/' + deviceId + '/hour?sensorNumber=' + sensorNumber,
            dataType: "json",
            success: function(response){
                plot = $.plot($(chartContainer), [{color: 'green', data: mapData(response.data)}], {
                    series: {
                        lines: {show: true, fill: 0.15, lineWidth: 4}
                    }
                });
            }
        });
    }
    function mapData(data){
        var result = [];
        for (var i = data.length; i > 0; i--) {
            result.push([i, (data[i]/100)])
        }
        return result;
    }
    function initChart(){
        plot = $.plot($(chartContainer), [{color: 'green', data: getData()}], {
            series: {
                lines: {show: true, fill: 0.15, lineWidth: 4}
            }
        });
        function getData() {
            if (data.length > 0)
                data = data.slice(1);

            while (data.length < totalPoints) {
                data.push(sensorData);
            }
            var result = [];
            for (var i = 0; i < data.length; i++) {
                result.push([i, data[i]])
            }
            return result;
        }
        function update() {
            var deviceId = $('.device-highlighted').text();
            var sensorNumber = $('input[name=sensorNumber]').val();
            if (updateCount == 9) {
                $.ajax({
                    url: contextPath + '/rs/data/get/' + deviceId + '?sensorNumber=' + sensorNumber,
                    dataType: "json",
                    success: function (response) {
                        document.getElementById('currentPowerHolder').innerHTML = response.data;
                        sensorData = response.data / 100;
                    }
                });
                updateCount = 0;
            }
            updateCount++;
            plot.setData([
                {color: 'green', data: getData()}
            ]);
            plot.draw();
            realTimeTimeout = setTimeout(update, 300);
        }
        update();
    }
});