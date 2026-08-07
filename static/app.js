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