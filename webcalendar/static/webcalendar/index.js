
function Calendar_Properties(Events, year, month, cur_year, cur_month, cur_day) {
    var t = document.getElementsByTagName("table")[0]
    var year_cal = !cur_month
    for (row = (year_cal ? 4 : 2); row < t.rows.length; row++) {
        var r = t.rows[row]
        for (cell = 0; cell < r.cells.length; cell++) {
            var c = r.cells[cell]
            var d = Number(c.innerText);
            //var cal_month = 
            if (d >= 1 && d <= 31) {
                c.style.setProperty("background-color", "lightgray")
                c.addEventListener("click", function() {
                    window.location.replace(`/${year}/${month}/${this.innerText}`)
                })
                if (year == cur_year && month == cur_month && d == cur_day) {
                    c.style.setProperty("background-color", "green")
                    c.style.setProperty("color", "white")
                }
                for (i = 0; i < Events.length; i++) {
                    if (d == Events[i]["day"]) {
                        c.style.setProperty("color", "rgb(237, 113, 113)")
                    }
                }
            } else {
                c.style.setProperty("background-color", "darkgray")
            }
        }
        
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const date = new Date();
    let cur_day = date.getDate();
    let cur_month = date.getMonth() + 1;
    let cur_year = date.getFullYear();
    document.getElementById("btn_today").addEventListener("click", () => {
        window.location.replace(`/${cur_year}/${cur_month}/${cur_day}`)
    })
    document.getElementById("btn_cur_month").addEventListener("click", () => {
        fetch(`getcalendar/${cur_year}/${cur_month}`).then(response => response.json()).then(x => {
            document.getElementById("calendar").innerHTML = x["calendar"]
            Calendar_Properties(x["Events"], cur_year, cur_month, cur_year, cur_month, cur_day)
        })
    })
/*     document.getElementById("btn_cur_year").addEventListener("click", () => {
        fetch(`getcalendar/${cur_year}`).then(response => response.json()).then(x => {
            document.getElementById("calendar").innerHTML = x["calendar"]
            console.log(x["calendar"])
            Calendar_Properties(x["Events"], year, undefined, cur_year, cur_month, cur_day)
        })
    })
 */    document.getElementById("display").addEventListener("click", () => {
        var month = document.getElementById("month").value
        var year = document.getElementById("year").value
        fetch(`getcalendar/${year}/${month}`).then(response => response.json()).then(x => {
            document.getElementById("calendar").innerHTML = x["calendar"]
            Calendar_Properties(x["Events"], year, month, cur_year, cur_month, cur_day)
        })
    })
    
    fetch(`getcalendar/${cur_year}/${cur_month}`).then(response => response.json()).then(x => {
        Calendar_Properties(x["Events"], cur_year, cur_month, cur_year, cur_month, cur_day)
    })
})
