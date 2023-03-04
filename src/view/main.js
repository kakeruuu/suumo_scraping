function getData(url) {
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error(error);
        });
}

function createRegions() {
    getData("http://localhost:8000/read_region")
        .then(data => {
            const selectBox = document.getElementById("region_select_box");
            selectBox.innerHTML = `
                        <option value="">選択してください</option>
                        ${data.map(region => `<option value="${region.region_id}">${region.region}</option>`).join("")}
                    `;
        })
        .catch(error => {
            console.error(error);
        })
}

// 以下をセレクトボックスに変更し都道府県向けの関数に変換する
function createPrefecturesSelectBox() {
    const regionSelectBox = document.getElementById("region_select_box");
    const prefecturesCheckBox = document.getElementById("prefecture_selectbox");
    const regionId = regionSelectBox.value;

    if (!regionId) {
        prefecturesCheckBox.innerHTML = "";
        return;
    }

    getData(`http://localhost:8000/read_prefecture?region_id=${regionId}`)
        .then(data => {
            const selectBox = document.getElementById("prefecture_select_box");
            selectBox.innerHTML = `
                        <option value="">選択してください</option>
                        ${data.map(prefecture => `<option value="${prefecture.prefecture_id}">${prefecture.prefecture}</option>`).join("")}
                    `;
        })
        .catch(error => {
            console.error(error);
        })
}


function createCityGroups() {
    const cityCheckBox = document.getElementById("city_checkboxes")
    const prefecturesSelectBox = document.getElementById("prefecture_select_box")
    const prefecturesId = prefecturesSelectBox.value;

    if (!prefecturesId) {
        prefecturesCheckBox.innerHTML = "";
        return;
    }

    getData(`http://localhost:8000/read_prefecture?region_id=${regionId}`)
        .then(data => {
            const checkboxes = data.map(prefecture => {
                const label = document.createElement("label");
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.name = "prefecture[]";
                checkbox.value = prefecture.prefecture_id;
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(prefecture.prefecture));
                return label;
            });

            prefecturesCheckBox.innerHTML = "";
            checkboxes.forEach(checkbox => {
                prefecturesCheckBox.appendChild(checkbox);
            });
        })
        .catch(error => {
            console.error(error);
        });
}

window.onload = function () {
    createRegions()
}