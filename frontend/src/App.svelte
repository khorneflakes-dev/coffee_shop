<script>
// @ts-nocheck

  import './lib/Tailwind.css'
  import { onMount } from 'svelte';

  let jsonData = null;
  let formData = {
    text: '',
    is_done: false
  };
  let delete_id = '';

  async function fetchData() {
    const response = await fetch('http://localhost:8000');
    jsonData = await response.json();
  }

  onMount(() => {
    fetchData();
  });

  async function postData() {
    const response = await fetch('http://localhost:8000/create', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(formData)
    })
    // console.log(JSON.stringify(formData))
    formData.text = '';
    formData.is_done = false;
    fetchData();
  }

  async function deleteData(id) {
    const url = `http://localhost:8000/delete/${id}`;

    
    try {
      const response = await fetch(url ,{
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'}
      });
    }
    catch (error) {
      console.log('error al realizar la solicitud', error);
    }
    
    delete_id = '';
    fetchData();
  }

  let firstImage;
  let secondImage;
  let text_demo;

  async function handleSubmit() {
    const formData = new FormData();
    formData.append('file', firstImage);
    formData.append('fileb', secondImage);
    formData.append('token', text_demo);

    try {
      const response = await fetch('http://localhost:8000/files/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        alert('Imágenes guardadas exitosamente.');
        // Realiza alguna acción adicional si es necesario
      } else {
        alert('Error al guardar las imágenes.');
      }
    } catch (error) {
      console.error('Error al realizar la solicitud:', error);
    }
  }
</script>
<main class="bg-blue-200 text-center h-max">
{#if jsonData }
<table class="table-fixed">
  <tr>
    <td>id</td>
    <td>tarea</td>
    <td>estado</td>
  </tr>
  {#each Object.entries(jsonData) as [key, value]}
    <tr>
      <td>{value.id}</td>
      <td>{value.text}</td>
      <td>{value.is_done}</td>
      <!-- {#each Object.values(value) as value2}
        <td>{value2.id}</td>
      {/each} -->
    </tr>
  {/each}
</table>
{/if}
<div> 
  <p>agregar tarea:</p>
  <input bind:value={formData.text}/>
  <select bind:value={formData.is_done} >
    <option value=false>False</option>
    <option value=true>True</option>
  </select>
  <button type="button" on:click={postData}>Agregar</button>
</div>

<div>
  <p>borrar tarea:</p>
  <input bind:value={delete_id}/>
  <button type="button" on:click={() => deleteData(delete_id)}>Borrar</button>
</div>

<form on:submit|preventDefault={handleSubmit}>
  <input type="file" on:change={event => firstImage = event.target.files[0]} />
  <input type="file" on:change={event => secondImage = event.target.files[0]} />
  <input type="text" bind:value={text_demo}/>
  <button type="submit">Enviar</button>
</form>
<img src="http://localhost:8000/imagenes/e4a7c7d1-6366-4ace-a311-b063aac0de37.jpg" alt="">

</main>
