const API="http://127.0.0.1:8000";

loadRanking();
loadFoodStalls();
loadMenu();

async function loadRanking(){
    try{
        const response=await fetch(`${API}/ranking/`);
        const data=await response.json();

        const div=document.getElementById("ranking");
        div.innerHTML="";

        if(data.length===0){
            div.innerHTML="<p>No hay reseñas todavía.</p>";
            return;
        }

        data.forEach(item=>{
            div.innerHTML+=`
                <div class="card">
                    <h3>🏆 ${item.name}</h3>
                    <p>⭐ ${item.average_rating}</p>
                    <p>📝 ${item.total_reviews} reseñas</p>
                </div>
            `;
        });

    }catch(error){
        console.error(error);
    }
}

async function loadFoodStalls(){
    try{
        const response=await fetch(`${API}/food-stalls/`);
        const data=await response.json();

        const div=document.getElementById("food-stalls");
        div.innerHTML="";

        if(data.length===0){
            div.innerHTML="<p>No hay puestos registrados.</p>";
            return;
        }

        data.forEach(item=>{
            div.innerHTML+=`
                <div class="card">
                    <h3>${item.name}</h3>
                    <p>📍 ${item.location}</p>
                    <p>${item.description}</p>
                    <p>🕒 ${item.schedule}</p>
                    <p>📞 ${item.phone}</p>
                </div>
            `;
        });

    }catch(error){
        console.error(error);
    }
}

async function loadMenu(){
    try{
        const response=await fetch(`${API}/menu/`);
        const data=await response.json();

        const div=document.getElementById("menu");
        div.innerHTML="";

        if(data.length===0){
            div.innerHTML="<p>No hay platos registrados.</p>";
            return;
        }

        data.forEach(item=>{
            div.innerHTML+=`
                <div class="card">
                    <h3>${item.name}</h3>
                    <p>💰 ${item.price} Bs</p>
                    <p>${item.available ? "✅ Disponible" : "❌ No disponible"}</p>
                </div>
            `;
        });

    }catch(error){
        console.error(error);
    }
}