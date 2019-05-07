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
$(document).ready(
    function() {
        // init
        if (document.getElementById('id_shape_0').checked) {
            $("#div_id_radius").show();
            $("#div_id_width").hide();
            $("#div_id_height").hide();
            $("#div_id_polygon").hide();
        } else if (document.getElementById('id_shape_1').checked) {
            $("#div_id_radius").hide();
            $("#div_id_width").show();
            $("#div_id_height").show();
            $("#div_id_polygon").hide();
        } else {
            $("#div_id_radius").hide();
            $("#div_id_width").hide();
            $("#div_id_height").hide();
            $("#div_id_polygon").show();
        }
        if (document.getElementById('id_name_coord_0').checked) {
            $("#div_id_name").show();
            $("#div_id_ra").hide();
            $("#div_id_dec").hide();
            $("#div_id_input_file").hide();
            $("#div_id_adql").hide()
            $("#data-form").show();
        } else if (document.getElementById('id_name_coord_1').checked) {
            $("#div_id_name").hide();
            $("#div_id_ra").show();
            $("#div_id_dec").show();
            $("#div_id_input_file").hide();
            $("#div_id_adql").hide()
            $("#data-form").show();
        } else if (document.getElementById('id_name_coord_2').checked) {
            $("#div_id_name").hide();
            $("#div_id_ra").hide();
            $("#div_id_dec").hide();
            $("#div_id_input_file").show();
            $("#div_id_adql").hide()
            $("#data-form").hide();
        } else if (document.getElementById('id_name_coord_3').checked) {
            $("#div_id_name").hide();
            $("#div_id_ra").hide();
            $("#div_id_dec").hide();
            $("#div_id_input_file").hide();
            $("#div_id_adql").show();
            $("#data-form").hide();
        }
        var positional = document.getElementById('id_positional_images_0');
        if (positional != null) {
            if (positional.checked) {
                $("#div_id_instrument").hide();
                $("#div_id_level").hide();
                $("#div_id_table").show();
            } else {
                $("#div_id_instrument").show();
                $("#div_id_level").show();
                $("#div_id_table").hide();
            }
        }
        var dr = document.getElementById('id_data_release_0');
        if (dr != null) {
            if (dr.checked) {
                $("#div_id_table").show();
                $("#div_id_table_dr2").hide();
            } else {
                $("#div_id_table").hide();
                $("#div_id_table_dr2").show();
            }
        }
        // on change
        $("#id_shape_0").change(
            function() {
                //$('label[for=id_ra], input#id_ra').hide()
                $("#div_id_radius").show();
                $("#div_id_width").hide();
                $("#div_id_height").hide();
                $("#div_id_polygon").hide();
            });
        $("#id_shape_1").change(
            function() {
                $("#div_id_radius").hide();
                $("#div_id_width").show();
                $("#div_id_height").show();
                $("#div_id_polygon").hide();
            });
        $("#id_shape_2").change(
            function() {
                $("#div_id_radius").hide();
                $("#div_id_width").hide();
                $("#div_id_height").hide();
                $("#div_id_polygon").show();
            });
        $("#id_name_coord_0").change(
            function() {
                $("#div_id_name").show();
                $("#div_id_ra").hide();
                $("#div_id_dec").hide();
                $("#div_id_input_file").hide();
                $("#div_id_adql").hide();
                $("#data-form").show();
            });
        $("#id_name_coord_1").change(
            function() {
                $("#div_id_name").hide();
                $("#div_id_ra").show();
                $("#div_id_dec").show();
                $("#div_id_input_file").hide();
                $("#div_id_adql").hide();
                $("#data-form").show();
            });
        $("#id_name_coord_2").change(
            function() {
                $("#div_id_name").hide();
                $("#div_id_ra").hide();
                $("#div_id_dec").hide();
                $("#div_id_input_file").show();
                $("#div_id_adql").hide();
                $("#data-form").hide();
            });
        $("#id_name_coord_3").change(
            function() {
                $("#div_id_name").hide();
                $("#div_id_ra").hide();
                $("#div_id_dec").hide();
                $("#div_id_input_file").hide();
                $("#div_id_adql").show();
                $("#data-form").hide();
            });
        $("#id_positional_images_0").change(
            function() {
                $("#div_id_instrument").hide();
                $("#div_id_level").hide();
                $("#div_id_table").show();
            }
        );
        $("#id_positional_images_1").change(
            function() {
                $("#div_id_instrument").show();
                $("#div_id_level").show();
                $("#div_id_table").hide();
            }
        );
        $("#id_data_release_0").change(
            function() {
                $("#div_id_table").show();
                $("#div_id_table_dr2").hide();
            }
        );
        $("#id_data_release_1").change(
            function() {
                $("#div_id_table").hide();
                $("#div_id_table_dr2").show();
            }
        );
    });

$(document).ready(
    function() {
        $(".radio-circle").change(
            function() {
                $(".row-radius-input").show();
                $(".row-rectangle-input").hide();
                $(".row-polygon-input").hide();
            });
    });
$(document).ready(
    function() {
        $(".radio-rectangle").change(
            function() {
                $(".row-radius-input").hide();
                $(".row-rectangle-input").show();
                $(".row-polygon-input").hide();
            });
    });
$(document).ready(
    function() {
        $(".radio-polygon").change(
            function() {
                $(".row-radius-input").hide();
                $(".row-rectangle-input").hide();
                $(".row-polygon-input").show();
            });
    });

$(document).ready(
    function() {
        $("#gaia-tables-dropdown-menu li a").click(
            function() {
                $("#gaia-table-dropdown").text($(this).text());
                $("#gaia-table-dropdown").val($(this).val());
                var element = document.getElementById('gaia-table-input');
                if (element === null) {
                    var input = $("<input>")
                        .attr("type", "hidden")
                        .attr("id", "gaia-table-input")
                        .attr("name", "gaia-table-input").val($(this).text());
                    $("#gaia_query_form").append($(input));
                } else {
                    $("#gaia-table-input").val($(this).text());
                }
            });
    });

function set_titles(name_coord_titles, shape_titles, data_release_titles, positional_images_titles, instrument_titles) {
    let array_name_coord_titles = name_coord_titles.split(",");
    let array_shape_titles = shape_titles.split(",");
    let array_data_release_titles = [];
    let array_positional_images_titles = [];
    let array_instrument_titles = [];
    if (data_release_titles !== 0) {
        array_data_release_titles = data_release_titles.split(",");
    }
    if (positional_images_titles !== 0) {
        array_positional_images_titles = positional_images_titles.split(",");
    }
    if (instrument_titles !== 0) {
        array_instrument_titles = instrument_titles.split(",");
    }
    document.querySelector("label[for='id_name_coord_0']").setAttribute('title', array_name_coord_titles[0]);
    document.querySelector("label[for='id_name_coord_1']").setAttribute('title', array_name_coord_titles[1]);
    document.querySelector("label[for='id_name_coord_2']").setAttribute('title', array_name_coord_titles[2]);
    document.querySelector("label[for='id_name_coord_3']").setAttribute('title', array_name_coord_titles[3]);

    document.querySelector("label[for='id_shape_0']").setAttribute('title', array_shape_titles[0]);
    document.querySelector("label[for='id_shape_1']").setAttribute('title', array_shape_titles[1]);
    document.querySelector("label[for='id_shape_2']").setAttribute('title', array_shape_titles[2]);

    if (data_release_titles !== 0) {
        document.querySelector("label[for='id_data_release_0']").setAttribute('title', array_data_release_titles[0]);
        document.querySelector("label[for='id_data_release_1']").setAttribute('title', array_data_release_titles[1]);
    }

    if (positional_images_titles !== 0) {
        document.querySelector("label[for='id_positional_images_0']").setAttribute('title', array_positional_images_titles[0]);
        document.querySelector("label[for='id_positional_images_1']").setAttribute('title', array_positional_images_titles[1]);
    }

    if (instrument_titles !== 0) {
        document.querySelector("label[for='id_instrument_0']").setAttribute('title', array_instrument_titles[0]);
        document.querySelector("label[for='id_instrument_1']").setAttribute('title', array_instrument_titles[1]);
        document.querySelector("label[for='id_instrument_2']").setAttribute('title', array_instrument_titles[2]);
    }
}