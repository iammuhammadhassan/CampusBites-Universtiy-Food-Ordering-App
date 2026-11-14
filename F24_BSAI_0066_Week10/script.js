const orderForm = document.getElementById("orderForm");
const studentName = document.getElementById("studentName");
const studentEmail = document.getElementById("studentEmail");
const meal = document.getElementById("meal");
const currentTotal = document.getElementById("currentTotal");
const summaryTotal = document.getElementById("summaryTotal");
const orderSummary = document.getElementById("orderSummary");
const formMessage = document.getElementById("formMessage");
const placeOrder = document.getElementById("placeOrder");
const foodTip = document.getElementById("foodTip");

const getSelectedSize = () =>
    document.querySelector('input[name="size"]:checked');

const getSelectedExtras = () =>
    [...document.querySelectorAll(".extra:checked")];

const calculateTotal = () => {
    const mealPrice = Number(meal.selectedOptions[0]?.dataset.price || 0);
    const sizePrice = Number(getSelectedSize()?.dataset.price || 0);
    const extrasPrice = getSelectedExtras().reduce(
        (total, extra) => total + Number(extra.dataset.price),
        0
    );

    return mealPrice + sizePrice + extrasPrice;
};

const updateTotal = () => {
    const total = calculateTotal();
    currentTotal.textContent = `PKR ${total}`;
};

const showMessage = (message, type) => {
    formMessage.textContent = message;
    formMessage.className = `mt-3 mb-0 text-${type}`;
};

const fetchFoodTip = async () => {
    try {
        const response = await fetch(
            "https://www.themealdb.com/api/json/v1/1/random.php"
        );

        if (!response.ok) {
            throw new Error("Unable to fetch food tip.");
        }

        const data = await response.json();
        const randomMeal = data.meals?.[0];

        if (!randomMeal) {
            throw new Error("No food recommendation available.");
        }

        foodTip.textContent =
            `Try ${randomMeal.strMeal} for today's food inspiration!`;
    } catch (error) {
        foodTip.textContent =
            "Choose a balanced meal and enjoy your lunch!";
    }
};

const displayOrderSummary = () => {
    const selectedMeal = meal.selectedOptions[0];
    const selectedSize = getSelectedSize();
    const selectedExtras = getSelectedExtras();
    const total = calculateTotal();

    const items = [
        `${selectedMeal.value} — PKR ${selectedMeal.dataset.price}`,
        `${selectedSize.value} Size — PKR ${selectedSize.dataset.price}`,
        ...selectedExtras.map(
            extra => `${extra.value} — PKR ${extra.dataset.price}`
        )
    ];

    const heading = document.createElement("h5");
    heading.textContent = "Order Details";

    const nameLine = document.createElement("p");
    nameLine.textContent = `Student: ${studentName.value.trim()}`;

    const emailLine = document.createElement("p");
    emailLine.textContent = `Email: ${studentEmail.value.trim()}`;

    const list = document.createElement("ul");

    items.forEach(item => {
        const listItem = document.createElement("li");
        listItem.textContent = item;
        list.appendChild(listItem);
    });

    orderSummary.replaceChildren(heading, nameLine, emailLine, list);
    summaryTotal.textContent = `PKR ${total}`;
};

meal.addEventListener("change", updateTotal);

document.querySelectorAll('input[name="size"]').forEach(size => {
    size.addEventListener("change", updateTotal);
});

document.querySelectorAll(".extra").forEach(extra => {
    extra.addEventListener("change", updateTotal);
});

orderForm.addEventListener("submit", event => {
    event.preventDefault();

    if (!orderForm.checkValidity() || !meal.value) {
        orderForm.classList.add("was-validated");
        showMessage("Please complete all required fields correctly.", "danger");
        orderForm.reportValidity();
        return;
    }

    orderForm.classList.add("was-validated");
    displayOrderSummary();
    showMessage("Your order has been placed successfully!", "success");
});

fetchFoodTip();
updateTotal();
