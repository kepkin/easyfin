function Calendar() {
    "use strict";
    this.dateValue = new Date();

    this.nextMonth = function() {
        var cur_m = this.dateValue.getMonth();
        var cur_y = this.dateValue.getFullYear();
        if (cur_m === 11) {
            cur_y = cur_y + 1;
            cur_m = 1;
        } else {
            cur_m = cur_m + 2;
        }

        this.dateValue = new Date(cur_y, cur_m, 0);
    };

    this.prevMonth = function() {
        var cur_m = this.dateValue.getMonth();
        var cur_y = this.dateValue.getFullYear();
        if (cur_m === 0) {
            cur_y = cur_y - 1;
            cur_m = 12;
        }

        this.dateValue = new Date(cur_y, cur_m, 0);
    };
}
