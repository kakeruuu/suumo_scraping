const fetchData = async (url) => {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}

const createRegions = async () => {
    const data = await fetchData("http://localhost:8000/read_region");
    const selectBox = document.getElementById("region_select_box");
    selectBox.innerHTML = `
        <option value="">選択してください</option>
        ${data.map(region => `<option id="${region.region_id}" value="${region.region}">${region.region}</option>`).join("")}
    `;
}

const createPrefecturesSelectBox = async () => {
    const regionSelectBox = document.getElementById("region_select_box");
    const prefecturesSelectBox = document.getElementById("prefecture_select_box");
    const regionId = regionSelectBox.options[regionSelectBox.selectedIndex].id;

    if (!regionId) {
        prefecturesSelectBox.innerHTML = "";
        return;
    }

    const data = await fetchData(`http://localhost:8000/read_prefecture?region_id=${regionId}`);
    prefecturesSelectBox.innerHTML = `
        <option value="">選択してください</option>
        ${data.map(prefecture => `<option id="${prefecture.prefecture_id}" value="${prefecture.prefecture}">${prefecture.prefecture}</option>`).join("")}
    `;
}

const createCityCheckBoxes = async () => {
    const prefecturesSelectBox = document.getElementById("prefecture_select_box");
    const prefectureId = prefecturesSelectBox.options[prefecturesSelectBox.selectedIndex].id
    const cityGroupUrl = `http://localhost:8000/read_city_group?prefecture_id=${prefectureId}`;
    const cityGroupJson = await fetchData(cityGroupUrl);

    const trs = await Promise.all(cityGroupJson.map(async (group) => {
        const cityUrl = `http://localhost:8000/read_city?group_id=${group.group_id}`;
        const cityJson = await fetchData(cityUrl);

        const cities = cityJson.map(city => `
            <label>
                <input type="checkbox" name="main_conditions" value="${city.city}">
                ${city.city}
            </label>
        `).join('');

        const citiesTd = `<td>${cities}</td>`;
        const groupTh = `<th><label><input type="checkbox">${group.city_group}</label></th>`;
        return `<tr>${groupTh}${citiesTd}</tr>`;
    }));

    const table = document.createElement('table');
    const tbody = document.createElement('tbody');
    tbody.innerHTML = trs.join('');
    table.appendChild(tbody);

    const cityCheckBoxes = document.getElementById("city_checkboxes");
    const existingTable = cityCheckBoxes.querySelector("table");
    if (existingTable) {
        existingTable.remove();
    }
    cityCheckBoxes.appendChild(table);

    const ths = table.querySelectorAll("th");
    for (const th of ths) {
        th.addEventListener("click", () => {
            const isChecked = th.querySelector("input").checked;
            const inputs = th.parentElement.querySelectorAll("td input");
            for (const input of inputs) {
                if (input) {
                    input.checked = isChecked;
                }
            }
        });
    }
}

const submitForm = async () => {
    try {
        const formData = new FormData(document.querySelector('form'));
        const data = {};
        const other_conditions = { 間取りタイプ: [], 建物種別: [] };
        for (const [key, value] of formData.entries()) {
            if (key === '間取りタイプ') {
                other_conditions['間取りタイプ'].push(value);
                continue;
            }
            if (key === '建物種別') {
                other_conditions['建物種別'].push(value);
                continue;
            }
            if (!data[key]) {
                data[key] = value;
                continue;
            }
            if (!Array.isArray(data[key])) {
                data[key] = [data[key]];
            }
            data[key].push(value);
        }
        data['other_conditions'] = other_conditions;
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        };
        const response = await fetch('http://localhost:8000/test', requestOptions);
        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }
        const responseData = await response.json();
        console.log(responseData);
    } catch (error) {
        console.error(error);
    }
};


window.onload = async () => {
    await createRegions();
}
