$(function(){
    var base_url = document.getElementById("base_url").value;

    fetch( base_url + '/get_my_transactions/')
      .then((response) => {

        return response.json();
      })
      .then((data) => {

        var transactions = data.transactions;

        let list = document.getElementById("myList");

        if (transactions.length ==0){

            let li = document.createElement("li");
            li.innerText = "Keine Einträge gefunden!";
            list.appendChild(li);
        }


                  var table = document.createElement("table"), row, cellA, cellB;
                  document.getElementById("demoA").appendChild(table);
                                      var header = table.createTHead();


                    row = header.insertRow();

                    cellAA = row.insertCell();
                    cellAA.innerHTML = "<b>Autonummer</b>";

                    cellAA = row.insertCell();
                    cellAA.innerHTML = "<b>Kilometerstand</b>";

                    cellAA = row.insertCell();
                    cellAA.innerHTML = "<b>Tagse-Kilometer</b>";

                    cellAA = row.insertCell();
                    cellAA.innerHTML = "<b>Datum</b>";

                    cellAA = row.insertCell();
                    cellAA.innerHTML = "<b>Liter</b>";

                    cellAA = row.insertCell();
                    cellAA.innerHTML = "<b>Preis</b>";
        transactions.forEach((item)=>{

                    row = table.insertRow();

                    cellA = row.insertCell();
                    cellB = row.insertCell();
                    cellC = row.insertCell();
                    cellD = row.insertCell();
                    cellE = row.insertCell();
                    cellF = row.insertCell();


                    cellA.innerHTML = item.car;
                    cellB.innerHTML = item.current_mileage;
                    cellC.innerHTML = item.daily_mileage;
                    cellD.innerHTML = item.date;
                    cellE.innerHTML = item.liter;
                    cellF.innerHTML = item.price;


                });

      });

});