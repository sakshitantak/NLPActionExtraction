var pythonShell = require("python-shell")
var path = require("path")

function get_information_json() {

    var sentence = document.getElementById("sentence_input").value

    //type_input is the dropdown
    var option = document.getElementById("type_input").value
    
    document.getElementById("sentence_input").value = ""

    var options = {
        scriptPath: path.join(__dirname, '/engine'),
        //args : [sentence]
        args: [sentence, option]
    }

    pythonShell.PythonShell.run('extract_info.py', options, function (error, result) {
        if (error) throw error
        console.log(result[0])
        var jsonResult = JSON.parse(result[0])

        document.getElementById("tid-out").innerHTML = jsonResult["case_id"];
        document.getElementById("action-out").innerHTML = jsonResult["action"];
        document.getElementById("expec-out").innerHTML = jsonResult["expectation"];
        document.getElementById("type-out").innerHTML = jsonResult["type"]; //? "Unique" : "General";
        
        //test on console what is returned on front end
        console.log(jsonResult["type"])
        
        var tokensFormatted = ""
        for (var i = 0; i < jsonResult["tokens"].length; i++) {
            tokensFormatted += '<span class="token-style">' + jsonResult["tokens"][i] + '</span>'
        }
        document.getElementById("tokens").innerHTML = tokensFormatted

        if (jsonResult["predictions"].length > 0) {
            var listItems = "<ul style=\"list-style-type:disc;\">"
            for (var i = 0; i < jsonResult["predictions"].length; i++) {
                listItems += '<span class="token-style">' + jsonResult["predictions"][i] + '</span>'
            }
            listItems += "</ul>"
            document.getElementById("suggestions").innerHTML = listItems

            document.getElementById("suggestions").style.display = "block"
            document.getElementById("suggestionsTitle").style.display = "block"
        } else {
            document.getElementById("suggestions").style.display = "none"
            document.getElementById("suggestionsTitle").style.display = "none"
        }

        if (jsonResult["inputs"].length > 0) {
            var finalStr = '<table border="1" style="width:80%;margin: auto;"><tr><td style="text-align: center">Test Input Name</td><td style="text-align: center">Test Data Value</td></tr>';
            jsonResult["inputs"].forEach((ele) => {
                finalStr += "<tr><td style=\"text-align: center\">" + ele[0] + "</td><td>" + ele[1] + "</td></tr>";
            });
            finalStr += "</table>";
            document.getElementById("inputs-out").innerHTML = finalStr;
        } else {
            document.getElementById("inputs-out").innerHTML = "-";
        }


        document.getElementById("output-div").style.display = "block"
    })
}
