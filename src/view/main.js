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
        ${data.map(region => `<option value="${region.region_id}">${region.region}</option>`).join("")}
    `;
}

const createPrefecturesSelectBox = async () => {
    const regionSelectBox = document.getElementById("region_select_box");
    const prefecturesSelectBox = document.getElementById("prefecture_select_box");
    const regionId = regionSelectBox.value;

    if (!regionId) {
        prefecturesSelectBox.innerHTML = "";
        return;
    }

    const data = await fetchData(`http://localhost:8000/read_prefecture?region_id=${regionId}`);
    prefecturesSelectBox.innerHTML = `
        <option value="">選択してください</option>
        ${data.map(prefecture => `<option value="${prefecture.prefecture_id}">${prefecture.prefecture}</option>`).join("")}
    `;
}

const createCityCheckBoxes = async () => {
    const prefecturesSelectBox = document.getElementById("prefecture_select_box");
    const prefectureId = prefecturesSelectBox.value
    const cityGroupUrl = `http://localhost:8000/read_city_group?prefecture_id=${prefectureId}`;
    const cityGroupJson = await fetchData(cityGroupUrl);

    const trs = await Promise.all(cityGroupJson.map(async (group) => {
        const cityUrl = `http://localhost:8000/read_city?group_id=${group.group_id}`;
        const cityJson = await fetchData(cityUrl);

        const cities = cityJson.map(city => `
            <label>
                <input type="checkbox" name="${city.city}" value="${city.city_id}">
                ${city.city}
            </label>
        `).join('');

        const citiesTd = `<td>${cities}</td>`;
        const groupTh = `<th><label><input type="checkbox" name="${group.city_group}" value="${group.group_id}">${group.city_group}</label></th>`;
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

window.onload = async () => {
    await createRegions();
}
