;
$(function () {
    var contextPath = $('#contextPath').data('contextpath');
    function postData() {
        var deviceId = $('input[name=deviceId]').val();
        $.ajax({url: contextPath + '/rs/data/post/' + deviceId + '/' + '0F30'+(Math.floor(Math.random()*1000)+1000)+'0001222233334444555566667777'
        });
        if ($('input[name=doGet]').is(':checked')) {
            $.ajax({url: contextPath + '/rs/data/get/' + deviceId});
        }
        var delay = $('input[name=delay]').val();
        setTimeout(postData, delay);
    }
    setTimeout(postData, 1000);
});