function formatDateToDDMMYYYY(t){t=new Date(t);return("0"+t.getDate()).slice(-2)+`-${("0"+(t.getMonth()+1)).slice(-2)}-`+t.getFullYear()}$(document).ready(function(){formatDateToDDMMYYYY(new Date);$("#datatable-buttons").DataTable({responsive:!1,scrollX:!0}).buttons().container().insertBefore("#datatable-buttons_wrapper .dataTables_length"),$(".dataTables_length select").addClass("form-select form-select-sm"),$("#datatable-buttons_wrapper .form-check").on("click",function(t){t.stopPropagation()})});