/*
Template Name: Skote - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: Datatables Js File
*/

function formatDateToDDMMYYYY(date) {
  const d = new Date(date);
  const day = ("0" + d.getDate()).slice(-2); // Add leading zero if day is less than 10
  const month = ("0" + (d.getMonth() + 1)).slice(-2); // Months are 0-indexed. Add leading zero if month is less than 10
  const year = d.getFullYear();

  return `${day}-${month}-${year}`;
}

$(document).ready(function () {
  //Buttons examples
  const currentDate = new Date();
  const formattedDate = formatDateToDDMMYYYY(currentDate);

  var table,
    option = {
      // lengthChange: false,
      buttons: [
        "copy",
        {
          extend: "excel",
          filename: "Granit AI data export " + formattedDate, // Sets the file name when downloading
        },
        "pdf",
        {
          text: "Extract",
          tag: "a",
          attr: {
            href: "?extract=true",
          },
          action: function (e, dt, node, config) {
            window.location.href = $(e.currentTarget).attr("href");
          },
        },
        {
          text: "Audit Summary",
          action: function (e, dt, node, config) {
            alert("Audit Summary");
          },
        },
        {
          text: "Clear Selected",
          action: function (e, dt, node, config) {
            $('#datatable-buttons input[type="checkbox"]:checked').prop(
              "checked",
              false
            );
          },
        },
        // {
        //   text: "Add Column",
        //   action: function (e, dt, node, config) {
        //     // Destroy the existing table
        //     table.destroy();

        //     // Add the new column to the headers programmatically (optional if not added manually to DOM)
        //     $("#datatable-buttons").find("thead tr").append("<th>New Col</th>");
        //     $("#datatable-buttons")
        //       .find("tbody tr")
        //       .append("<td>New Data</td>");

        //     // Reinitialize the table
        //     table = $("#datatable-buttons").DataTable(option);

        //     table
        //       .buttons()
        //       .container()
        //       .insertBefore("#datatable-buttons_wrapper .dataTables_length");
        //     $(".dataTables_length select").addClass(
        //       "form-select form-select-sm"
        //     );
        //   },
        // },
      ],
      responsive: false,
      scrollX: true,
    };
  table = $("#datatable-buttons").DataTable(option);

  table
    .buttons()
    .container()
    .insertBefore("#datatable-buttons_wrapper .dataTables_length");

  $(".dataTables_length select").addClass("form-select form-select-sm");
  $("#datatable-buttons_wrapper .form-check").on("click", function (e) {
    // e.preventDefault();
    e.stopPropagation();
  });
});
