/*
Copyright (C) 2016-2018 Quasar Science Resources, S.L.

This file is part of DEAVI.

DEAVI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DEAVI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DEAVI.  If not, see <http://www.gnu.org/licenses/>.
*/
/*$(document).ready(function() {
    function myFunction(x) {

        if (x.matches) { // If media query matches
            var contenido = document.getElementById("AASubmenu");
            var contenido2 = document.getElementById("QQSubmenu");
            var contenido3 = document.getElementById("DDSubmenu");
            var contenido4 = document.getElementById("helpmenu");
            console.log(contenido);
            console.log(contenido2);
            console.log(contenido3);
            console.log(contenido4);
            var element = document.getElementsByClassName("li-id");
            console.log(element);
            var create, create_i, create2, create_i2, create3, create_i3, create4, create_i4;


            create = document.createElement("a");
            create.className += "dropdown-toggle a-menu";
            create.setAttribute("data-toggle", "collapse");
            create.setAttribute("aria-expanded", "false");
            create.setAttribute("onclick", "menu(1)");
            create_i = document.createElement("i");
            create.href = "#ASubmenu";
            create.id = "AASubmenu";
            create_i.className += "fas fa-list";

            create2 = document.createElement("a");
            create2.className += "dropdown-toggle a-menu";
            create2.setAttribute("data-toggle", "collapse");
            create2.setAttribute("aria-expanded", "false");
            create2.setAttribute("onclick", "menu(2)");
            create_i2 = document.createElement("i");
            create2.href = "#QSubmenu";
            create2.id = "QQSubmenu";
            create_i2.className += "fab fa-envira fa-flip-horizontal";

            create3 = document.createElement("a");
            create3.className += "dropdown-toggle a-menu";
            create3.setAttribute("data-toggle", "collapse");
            create3.setAttribute("aria-expanded", "false");
            create3.setAttribute("onclick", "menu(3)");
            create_i3 = document.createElement("i");
            create3.href = "#DSubmenu";
            create3.id = "DDSubmenu";
            create_i3.className += "fas fa-hdd";

            create4 = document.createElement("a");
            create4.className += "dropdown-toggle a-menu";
            create4.setAttribute("data-toggle", "collapse");
            create4.setAttribute("aria-expanded", "false");
            create4.setAttribute("onclick", "menu(4)");
            create_i4 = document.createElement("i");
            create4.href = "#AbSubmenu";
            create4.id = "helpmenu";
            create_i4.className += "fas fa-question-circle";

            create.appendChild(create_i);
            create2.appendChild(create_i2);
            create3.appendChild(create_i3);
            create4.appendChild(create_i4);

            if (contenido.getAttribute("aria-expanded") === "true") {
                create.setAttribute("aria-expanded", "true");
                create2.setAttribute("aria-expanded", "false");
                create3.setAttribute("aria-expanded", "false");
                create4.setAttribute("aria-expanded", "false");
                console.log(create);
                console.log(create2);
            } else if (contenido2.getAttribute("aria-expanded") === "true") {
                create.setAttribute("aria-expanded", "false");
                create2.setAttribute("aria-expanded", "true");
                create3.setAttribute("aria-expanded", "false");
                create4.setAttribute("aria-expanded", "false");
            } else if (contenido3.getAttribute("aria-expanded") === "true") {
                create.setAttribute("aria-expanded", "false");
                create2.setAttribute("aria-expanded", "false");
                create3.setAttribute("aria-expanded", "true");
                create4.setAttribute("aria-expanded", "false");
            } else if (contenido4.getAttribute("aria-expanded") === "true") {
                create.setAttribute("aria-expanded", "false");
                create2.setAttribute("aria-expanded", "false");
                create3.setAttribute("aria-expanded", "false");
                create4.setAttribute("aria-expanded", "true");
            } else {
                create.setAttribute("aria-expanded", "false");
                create2.setAttribute("aria-expanded", "false");
                create3.setAttribute("aria-expanded", "false");
                create4.setAttribute("aria-expanded", "false");
            }

            contenido.parentNode.removeChild(contenido);
            contenido2.parentNode.removeChild(contenido2);
            contenido3.parentNode.removeChild(contenido3);
            contenido4.parentNode.removeChild(contenido4);

            var element_ul = document.getElementById("ASubmenu");
            var element_ul2 = document.getElementById("QSubmenu");
            var element_ul3 = document.getElementById("DSubmenu");
            var element_ul4 = document.getElementById("AbSubmenu");

            element[0].insertBefore(create, element_ul);
            element[1].insertBefore(create2, element_ul2);
            element[2].insertBefore(create3, element_ul3);
            element[3].insertBefore(create4, element_ul4);
            /*let height_aux = $('#sidebar').height();
            height_aux += "px";
            console.log(height_aux);
            document.getElementById("card").style.height = height_aux;*/
/*<a href="#ASubmenu" data-toggle="collapse" aria-expanded="false"
            class="dropdown-toggle a-menu"><i class="fas fa-list"></i> Algorithms</a>
            contenido.className = contenido.className.replace("col-sm-8", "col-sm-12");
            console.log(contenido);
        } else {
            var contenido = document.getElementById("AASubmenu");
            var contenido2 = document.getElementById("QQSubmenu");
            var contenido3 = document.getElementById("DDSubmenu");
            var contenido4 = document.getElementById("helpmenu");

            var text = document.createTextNode(" Algorithms");
            var text2 = document.createTextNode(" Queries");
            var text3 = document.createTextNode(" Data");
            var text4 = document.createTextNode(" Help");

            contenido.appendChild(text);
            contenido2.appendChild(text2);
            contenido3.appendChild(text3);
            contenido4.appendChild(text4);
            /*let height_aux = $('#sidebar').height();
            height_aux += "px";
            console.log(height_aux);
            document.getElementById("card").style.height = height_aux;*/
/*}

    }

    var x = window.matchMedia("(max-width: 1032px)")
    myFunction(x) // Call listener function at run time
    x.addListener(myFunction);
});*/

/*function menu(num) {
    var AASubmenu = document.getElementById("AASubmenu");
    var ASubmenu = document.getElementById("ASubmenu");
    var QQSubmenu = document.getElementById("QQSubmenu");
    var QSubmenu = document.getElementById("QSubmenu");
    var DDSubmenu = document.getElementById("DDSubmenu");
    var DSubmenu = document.getElementById("DSubmenu");
    var helpmenu = document.getElementById("helpmenu");
    var AbSubmenu = document.getElementById("AbSubmenu");

    if (num === 1) {
        if (AASubmenu.getAttribute("aria-expanded") === "true") {
            AASubmenu.setAttribute("aria-expanded", "false");
        } else {
            AASubmenu.setAttribute("aria-expanded", "true");
            AASubmenu.className = "dropdown-toggle a-menu";
        }


        QQSubmenu.setAttribute("aria-expanded", "false");
        QQSubmenu.className = "dropdown-toggle a-menu collapsed";
        QSubmenu.className = "collapsing list-unstyled";

        DDSubmenu.setAttribute("aria-expanded", "false");
        DDSubmenu.className = "dropdown-toggle a-menu collapsed";
        DSubmenu.className = "collapsing list-unstyled";

        helpmenu.setAttribute("aria-expanded", "false");
        helpmenu.className = "dropdown-toggle a-menu collapsed";
        AbSubmenu.className = "collapsing list-unstyled";

        var delayInMilliseconds = 500;
        setTimeout(function() {
            QSubmenu.className = "collapse list-unstyled";
            DSubmenu.className = "collapse list-unstyled";
            AbSubmenu.className = "collapse list-unstyled";
        }, delayInMilliseconds);

    } else if (num === 2) {
        if (QQSubmenu.getAttribute("aria-expanded") === "true") {
            QQSubmenu.setAttribute("aria-expanded", "false");
        } else {
            QQSubmenu.setAttribute("aria-expanded", "true");
            QQSubmenu.className = "dropdown-toggle a-menu";
        }

        AASubmenu.setAttribute("aria-expanded", "false");
        AASubmenu.className = "dropdown-toggle a-menu collapsed";
        ASubmenu.className = "collapsing list-unstyled";

        DDSubmenu.setAttribute("aria-expanded", "false");
        DDSubmenu.className = "dropdown-toggle a-menu collapsed";
        DSubmenu.className = "collapsing list-unstyled";

        helpmenu.setAttribute("aria-expanded", "false");
        helpmenu.className = "dropdown-toggle a-menu collapsed";
        AbSubmenu.className = "collapsing list-unstyled";

        var delayInMilliseconds = 500;
        setTimeout(function() {
            ASubmenu.className = "collapse list-unstyled";
            DSubmenu.className = "collapse list-unstyled";
            AbSubmenu.className = "collapse list-unstyled";
        }, delayInMilliseconds);
    } else if (num === 3) {
        if (DDSubmenu.getAttribute("aria-expanded") === "true") {
            DDSubmenu.setAttribute("aria-expanded", "false");
        } else {
            DDSubmenu.setAttribute("aria-expanded", "true");
            DDSubmenu.className = "dropdown-toggle a-menu";
        }

        QQSubmenu.setAttribute("aria-expanded", "false");
        QQSubmenu.className = "dropdown-toggle a-menu collapsed";
        QSubmenu.className = "collapsing list-unstyled";

        AASubmenu.setAttribute("aria-expanded", "false");
        AASubmenu.className = "dropdown-toggle a-menu collapsed";
        ASubmenu.className = "collapsing list-unstyled";

        helpmenu.setAttribute("aria-expanded", "false");
        helpmenu.className = "dropdown-toggle a-menu collapsed";
        AbSubmenu.className = "collapsing list-unstyled";

        var delayInMilliseconds = 500;
        setTimeout(function() {
            QSubmenu.className = "collapse list-unstyled";
            ASubmenu.className = "collapse list-unstyled";
            AbSubmenu.className = "collapse list-unstyled";
        }, delayInMilliseconds);
    } else if (num === 4) {
        if (helpmenu.getAttribute("aria-expanded") === "true") {
            helpmenu.setAttribute("aria-expanded", "false");
        } else {
            helpmenu.setAttribute("aria-expanded", "true");
            helpmenu.className = "dropdown-toggle a-menu";
        }

        QQSubmenu.setAttribute("aria-expanded", "false");
        QQSubmenu.className = "dropdown-toggle a-menu collapsed";
        QSubmenu.className = "collapsing list-unstyled";

        DDSubmenu.setAttribute("aria-expanded", "false");
        DDSubmenu.className = "dropdown-toggle a-menu collapsed";
        DSubmenu.className = "collapsing list-unstyled";

        AASubmenu.setAttribute("aria-expanded", "false");
        AASubmenu.className = "dropdown-toggle a-menu collapsed";
        ASubmenu.className = "collapsing list-unstyled";

        var delayInMilliseconds = 500;
        setTimeout(function() {
            QSubmenu.className = "collapse list-unstyled";
            DSubmenu.className = "collapse list-unstyled";
            ASubmenu.className = "collapse list-unstyled";
        }, delayInMilliseconds);
    }
}*/

function breadcrumb(directoryname) {
    //var bc_construc;
    //console.log(directoryname.id);
    if (directoryname.id == "") {
        //console.log(directoryname.id);
        localStorage("bc_contruc", document.id);
    } else if (directoryname.id == "results") {
        //console.log(directoryname.id);
        localStorage("bc_contruc", document.id);
    } else if (directoryname.id == "user") {
        //console.log(directoryname.id);
        localStorage("bc_contruc", document.id);
    } else if (directoryname.id == "gaia") {
        //console.log(directoryname.id);
        localStorage("bc_contruc", document.id);
    } else if (directoryname.id == "hsa") {
        //console.log(directoryname.id);
        localStorage("bc_contruc", document.id);
    }
}