function BootstrapDatePaginationController(elementId, observer) {
    "use strict";
    var selector = "#" + elementId;
    var parent = selector + " ul";
    var link = selector + " a";
    var current = new Calendar();
    var selected = {
        'm' : current.dateValue.getMonth(),
        'y' : current.dateValue.getFullYear()
    };

    function next() {
        current.nextMonth();
    }

    function prev() {
        current.prevMonth();
    }

    function getItemHtml(month, year) {
        var result = month == selected.m && year == selected.y ? "<li class='active'>"
                : "<li>";
        result = result + "<a href='#'>" + (month + 1) + "<br>" + year
                + "</a></li>";
        return result;
    }
    
    function addItemBack(month, year) {
        $(parent).prepend(getItemHtml(month, year));
    }

    function addItemForth(month, year) {
        $(parent).append(getItemHtml(month, year));
    }

    function build() {
        var calb = jQuery.extend(true, {}, current);
        var calf = jQuery.extend(true, {}, current);

        $(parent).html("");
        for (var i = 0; i < 3; i++) {
            calb.prevMonth();
            addItemBack(calb.dateValue.getMonth(), calb.dateValue
                    .getFullYear());
        }
        for (i = 0; i < 4; i++) {
            addItemForth(calf.dateValue.getMonth(), calf.dateValue
                    .getFullYear());
            calf.nextMonth();
        }
        $(parent).prepend("<li><a href='#'>&laquo;</a></li>");
        $(parent).append("<li><a href='#'>&raquo;</a></li>");

        bindEvents();
        observer.update(selected.y, selected.m + 1);
    }

    function bindEvents() {
        $(link).click(function() {
            if ($(this).text() === "«") {
                prev();
            } else if ($(this).html() === "»") {
                next();
            } else {
                var index = $(this).html().search("<br>");
                selected.m = $(this).html().substring(0, index) - 1;
                selected.y = $(this).html().substring(index + 4);
            }
            build();
        });
    }

    build();
}
