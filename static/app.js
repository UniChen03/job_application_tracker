const deleteDialog = document.querySelector("#delete-dialog");
const deleteForm = document.querySelector("#delete-form");
const deleteMessage = document.querySelector("#delete-message");
const cancelDeleteButton = document.querySelector("#cancel-delete");
const deleteButtons = document.querySelectorAll(".delete-button");

for (const deleteButton of deleteButtons) {
    deleteButton.addEventListener("click", () => {
        const company = deleteButton.dataset.company;
        const position = deleteButton.dataset.position;

        deleteMessage.textContent =
            `Delete the application for ${company} as ${position}?`;

        deleteForm.action = deleteButton.dataset.deleteUrl;
        deleteDialog.showModal();
    });
}

cancelDeleteButton.addEventListener("click", () => {
    deleteDialog.close();
});

function setRowEditing(row, isEditing) {
    const displayValues = row.querySelectorAll(".display-value");
    const editControls = row.querySelectorAll(".edit-control");
    const editLink = row.querySelector(".edit-link");
    const deleteButton = row.querySelector(".delete-button");
    const saveButton = row.querySelector(".save-edit-button");
    const cancelButton = row.querySelector(".cancel-edit-button");

    for (const displayValue of displayValues) {
        displayValue.hidden = isEditing;
    }

    for (const editControl of editControls) {
        editControl.hidden = !isEditing;
    }

    editLink.hidden = isEditing;
    deleteButton.hidden = isEditing;
    saveButton.hidden = !isEditing;
    cancelButton.hidden = !isEditing;
}

const editLinks = document.querySelectorAll(".edit-link");

for (const editLink of editLinks) {
    editLink.addEventListener("click", (event) => {
        event.preventDefault();

        const row = editLink.closest("tr");

        setRowEditing(row, true);
        row.querySelector(".edit-control").focus();
    });
}

const cancelEditButtons = document.querySelectorAll(".cancel-edit-button");

for (const cancelEditButton of cancelEditButtons) {
    cancelEditButton.addEventListener("click", () => {
        const row = cancelEditButton.closest("tr");
        const form = row.querySelector(".inline-edit-form");

        form.reset();
        setRowEditing(row, false);
    });
}