
function start_file_upload() {
    document.getElementById('fileid').click();
}
 var res = []

function on_file_selected(event) {
    var reader = new FileReader();
    //var result = [];
    //var that = this;
    //var option = document.getElementById('type_input').value

    reader.onload = function (evt) {
        //var result = [];
        lines = evt.target.result.split(/\r?\n/);
        console.log(lines);
        for (const line of lines){
            res.push(line);
            console.log(line);
        }
        //that.result = result;
        //console.log(result);
        window.value=res;
        //console.log(generateXML(window.value));
        //console.log(res);
    };
    //console.log(generateXML());
    //console.log(res);
    //generateXML(result);
    reader.onloadend = function () {
        //result = event.target.result;
        r = []
        r = window.value;
        //r = String(window.value);
        console.log(r);
        console.log(typeof(r));
        generateXML(r);
    }
    reader.readAsText(event.target.files[0]);
};

//console(generateXML());

function generateXML(input_arr) {

    console.log(input_arr);
    a = []
    for (const line of input_arr){
        a.push(line);
        //console.log(line);
    }
    console.log(a);
    var options = {
        scriptPath: path.join(__dirname, '/engine'),
        args : a
        //args: [inp_arr, option]
    }

    //var jsonResult = JSON.parse()
    pythonShell.PythonShell.run('try.py', options, function (error, result) {
        //var jsonResult = JSON.parse(result);
        //if (error) throw error
        console.log(result);
        console.log(typeof(result));
        console.log(error);
        //if (jsonResult['code'] == true) {
        //    console.log(jsonResult.input)
        //window.location = 'example.xlsx'
    })
}