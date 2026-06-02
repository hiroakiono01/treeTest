
    var dropzone=document.getElementById('dropzone');

    dropzone.ondrop=function(e){
    var myFile = document.getElementById('id_file');
    myFile.files=e.dataTransfer.files
    e.preventDefault();
    this.className='dropzone';
    //myFile=e.dataTransfer.files
    //console.log(myFile)
    };
    dropzone.ondragover=function(){
    this.className='dropzone dragover';
    return false;
    };
    dropzone.ondragleave=function(){
     this.className='dropzone';
     return false;
     };


    