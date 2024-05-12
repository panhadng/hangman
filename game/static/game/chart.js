window.onload = () => {
  google.charts.load("current", { packages: ["corechart", "bar"] });
  google.charts.setOnLoadCallback(drawBasic);
  function drawBasic() {
    var data = google.visualization.arrayToDataTable([
      ["Subject", "Score", { role: "style" }],
      ["Economics", 50, "#196b24"],
      ["Math", 40, "#46b1e1"],
      ["Politics", 35, "#46b1e1"],
      ["Physics", 30, "#46b1e1"],
      ["Commerce", 20, "#c00000"],
    ]);

    var options = {
      title: "Average Score by Categories",
      titleTextStyle: {
        color: "#FFF",
      },
      chartArea: { width: "60%", height: "90%" },
      backgroundColor: "none",
      hAxis: {
        textStyle: { color: "#FFF" },
        viewWindow: {
          min: 0,
          max: 50,
        },
      },
      vAxis: {
        textStyle: { color: "#FFF" },
      },
      legend: { position: "none" },
    };

    var chart = new google.visualization.BarChart(
      document.getElementById("chart")
    );

    chart.draw(data, options);
  }
};
