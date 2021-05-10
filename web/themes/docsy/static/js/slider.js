document.getElementById("slider").addEventListener("input", aktualisiere);
   function aktualisiere() {
	  var TS = (document.querySelector("input[name=a]"));
	  var b = '/pictures/exmouth_gulf/TS/ts_'+TS.value+'.png';
          document.getElementById("abb").setAttribute("src", b);
}
