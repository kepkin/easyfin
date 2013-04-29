function Expense(value) {
    var self = this;
    self.name = ko.observable(value.name);
    self.plan = ko.observable(value.plan);
    self.real = ko.observable(value.real);
    self.pk = value.pk;
    self.editing_name = ko.observable(false);
    self.editing_plan = ko.observable(false);
}

function ExpensesViewModel(url) {
    // Data
    var self = this;
    self.expenses = ko.observableArray([]);
    self.newExpenseValue = ko.observable("");

    self.getData = function() {
        self.expenses.removeAll();
        $.post(url.get, {
            'month' : self.month,
            'year' : self.year
        }, function(allData) {
            $.each(allData, function(index, value) {
                self.expenses.push(new Expense(value));
            });
        });
    };

    self.editItemName = function(item) {
        item.editing_name(true);
    };

    self.editItemPlan = function(item) {
        item.editing_plan(true);
    };

    self.stopEditing = function(item) {
        if (!item.editing_name() && !item.editing_plan())
            return;

        item.editing_name(false);
        item.editing_plan(false);
        item['month'] = self.month;
        item['year'] = self.year;

        $.post(url.update, item, function(data) {

        });
    };

    self.newExpense = function() {
        var newValue = self.newExpenseValue().trim()
        var lastSpace = newValue.lastIndexOf(" ");
        if (lastSpace == -1) {
            alert("invalid syntax");
            return;
        }

        var item = {};
        item['name'] = newValue.substr(0, lastSpace).trim();
        item['plan'] = newValue.substr(lastSpace + 1);
        item['real'] = "0.0";
        item['month'] = self.month;
        item['year'] = self.year;

        $.post(url.add, item, function(data) {

        });

        self.expenses.push(new Expense(item));
    };

    self.update = function(year, month) {
        self.year = year;
        self.month = month;
        self.getData();
    };
}