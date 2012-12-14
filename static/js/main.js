$(function () {
    "use strict";
    
    var months = ["January", "February", "March", "April", "May",
                "June", "July", "August", "September", "October",
                "November", "December"];


     // countries_request.done(function(msg) {
     //    alert("done!", msg);
     // });
    
    // $("#country").append(function (index, html) {
    // });

    $("#birth_year").append(function (index, html) {
        //Create a list of birth years to insert in the drop down box
        var str = "",
            today = new Date(),
            newest_year = today.getFullYear(),
            num_years = 110,
            current_year = newest_year;
        
        while (num_years >= 0) {
            str = str + "<option>" + current_year + "</option>";
            current_year -= 1;
            num_years -= 1;
        }
        
        return str;
    });
    
    $("#birth_month").append(function (index, html) {
        var i = 0,
            str = "";
        while (i < 12) {
            str = str + "<option>" + months[i] + "</option>";
            i += 1;
        }
        return str;
    });
    
    $("#birth_day").append(function (index, html) {
        var i = 1,
            str = "";
        while (i <= 31) {
            str = str + "<option>" + i + "</option>";
            i += 1;
        }
        return str;
    });
    
    function get_birthday_url() {
        var str = "",
            i = 0,
            month_string = $("#birth_month").val();
        
        while (i < 12) {
            if (months[i] === month_string) {
                break;
            }
            i += 1;
        }
        
        str = "/" + $("#country").val() +
            "/" + $("#gender").val() +
            "/" + $("#birth_year").val() +
            "/" + (i + 1) +
            "/" + $("#birth_day").val() + "/";
        return str;
    }
    
    function update_birthday_url() {
        $("#results_link").attr("href", get_birthday_url());
    }

    $.ajax({
         type: "GET",
         url: "countries/",
         dataType: "json",
         // success : function(data) {
         //      alert(data);
         // }
    }).done(function(data) {
        for (var i = 0; i < data.length; i++) {
            $("#country").append("<option>" + data[i].fields["country"] + "</option>");
        }
        update_birthday_url();
    });
    
    $("#country").change(update_birthday_url);
    $("#gender").change(update_birthday_url);
    $("#birth_day").change(update_birthday_url);
    $("#birth_month").change(update_birthday_url);
    $("#birth_year").change(update_birthday_url);
});



