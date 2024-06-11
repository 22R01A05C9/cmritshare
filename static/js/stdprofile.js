function changebtn() {
    $("#updateDetail").removeClass("disabled");
}

function uploadphoto(){
    xhr = new XMLHttpRequest();
    form = document.getElementById("cpp");
    formdata = new FormData(form);
    xhr.open("POST","/uploadpp");
    xhr.send(formdata);
    xhr.onload = () =>{
        res = xhr.response;
        console.log(res);
        if (res=="ok"){
            alert("Updated Successfully");
            window.location.href="/student";
        }else{
            alert("Some Error Occured")
        }
    }
}