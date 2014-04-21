function disableSumbit() {
		var elems = document.getElementsByName("removeShip");
		for (var j = 0; j < elems.length; j++) {
		  elems[j].disabled = true;
		};
	};

window.onload = disableSumbit;