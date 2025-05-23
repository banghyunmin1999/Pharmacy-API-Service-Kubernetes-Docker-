$(document).ready(function () {
  $("#collectBtn").click(function () {
    $.ajax({
      url: "/api/startCollecting",
      method: "GET",
      success: function (data) {
        $("#result").text(JSON.stringify(data, null, 2));
      },
      error: function () {
        alert("데이터 수집에 실패했습니다.");
      }
    });
  });
});

