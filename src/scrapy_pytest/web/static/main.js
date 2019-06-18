function filter() {
    $('#commit').on('click', function (e) {
        e.preventDefault();

        let storage = $('#storage').val();
        let spider = $('#spider').val();
        let parse_func = $('#parse_func').val();

        // superagent.get(`/?storage=${storage}&spider=${spider}&parse_func=${parse_func}`)
        superagent.get(`/filter?storage=${storage}`).end(function (err, data) {
            if (err) throw err;

            let json_data = JSON.parse(data.text);
            let str = '';
            for (let row of json_data.rows) {
                str = str + `<tr><td>${row.id}</td><td>${row.storage}</td><td>${row.spider}</td><td>${row.parse_func}</td><td>${row.url}</td><td>${JSON.stringify(row.meta)}</td></tr>`;
            }
            console.log(str);
            $('#content').html(str);
            $('.pagination').html('');
        });
    })
}

filter();