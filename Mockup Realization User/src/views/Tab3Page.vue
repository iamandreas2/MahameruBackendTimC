<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title><center>User</center></ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
     
      <ion-item fill="solid">
        <ion-input id="input" placeholder="First Name" class="custom"></ion-input>
      </ion-item>
    
      <ion-item fill="solid">
        <ion-input placeholder="Last Name" class="custom"></ion-input>
      </ion-item>
      
      <ion-item fill="outline">
        <ion-input placeholder="Phone Number" class="custom"></ion-input>
        
      </ion-item>
      
      <ion-item fill="outline">
       
      </ion-item>

      <center><button class="button" type="button">Save Changes</button></center>
      
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large"></ion-title>
        </ion-toolbar>
      </ion-header>
    
      <ExploreContainer name="" />
    </ion-content>
  </ion-page>
</template>

<style scoped>
ion-title{
  background-color: orange;
  color: black;
  height: 50px;

}
ion-input.custom {
  --background: #FFD384;
  --color: black;
  --placeholder-color: black;
  --placeholder-opacity: .8;

  --border-radius: 5px;
  --padding-bottom: 10px;
  --padding-end: 10px;
  --padding-start: 10px;
  --padding-top: 10px;
}

.button{
    background-color: orange;
    border: none;
    color: black;
    padding: 10px 30px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;

  }

  .custom{
  --background: #ff884b;
  --color: #000;
  --border-radius: 10px;
  --border-color: white;
  --border-style: solid;
  --border-width: 1px;
  --padding-top: 10px;
  --padding-bottom: 10px;
  margin-right: 10px;

}
  ion-item{
      align-items: center;
    }
</style>

<script lang="ts">
import { defineComponent } from 'vue';
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
import ExploreContainer from '@/components/ExploreContainer.vue';

export default  defineComponent({
  name: 'Tab1Page',
  components: { ExploreContainer, IonHeader, IonToolbar, IonTitle, IonContent, IonPage }
});
</script>