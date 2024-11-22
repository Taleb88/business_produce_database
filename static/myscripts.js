/*  window.addEventListener("load", function() {
    alert("Welcome to the Business Database");
  })
*/

function tableToCSV() {

    // variable stores final csv data prior to download
    let csv_data = [];

    // get each row of data
    let rows = document.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {

        // get each column
        let cols = rows[i].querySelectorAll('td,th');

        // store csv row of data
        let csvrow = [];
        for (let j = 0; j < cols.length; j++) {

            // Get text data of each cell of row and push it to csvrow
            csvrow.push(cols[j].innerHTML);
            }

            // combine each column value with comma
            csv_data.push(csvrow.join(","));
        }

        // combine each row data with new line character
        csv_data = csv_data.join('\n');

        // call this function to download csv
        downloadCSVFile(csv_data);
}

function downloadCSVFile(csv_data) {

        // csv file object created; csv_data fed into it
        CSVFile = new Blob([csv_data], {
            type: "text/csv"
        });

        // create temporary link to initiate download process
        let temp_link = document.createElement('a');

        // download csv
        temp_link.download = "confidential.csv";
        let url = window.URL.createObjectURL(CSVFile);
        temp_link.href = url;

        // link not to be displayed
        temp_link.style.display = "none";
        document.body.appendChild(temp_link);

        // click button to trigger download
        temp_link.click();
        document.body.removeChild(temp_link);
}

/*
// filter words
function myFunction() {
  let input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("userInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[0]; // Product
    td2 = tr[i].getElementsByTagName("td")[1]; // Price
    if (td1 || td2) {
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (txtValue1.toUpperCase().indexOf(filter) > -1 ||
            txtValue2.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
*/

// product search bar
function productSearch() {
    const search = document.getElementById('userInput').value.trim();
    const baseURL = window.location.origin + "/layout";
    window.location.href = `${baseURL}?search=${encodeURIComponent(search)}&page=1`;
}

function cursorToTheRight(x) {
    let value = x.value // get input value
    x.value = ' '; // value is temporarily cleared
    x.value = value + "" // restore value to move cursor to the right
    setTimeout("cursorToTheRight()", 200) // prevent lagging, allow page to load faster via user input
}
