<template>
  <div class="container">
    <h1>Contact</h1>
    <hr class="mt-5">
    <h3 class="mb-3">First, we need to know a little about yourself. Which of the following applies best to you?</h3>
    <b-form-select size="lg" block variant="secondary" v-model="selected" :options="options"></b-form-select>
    <component :is="selected"></component>
  </div>
</template>

<script>
import SpeakerContactForm from '@/components/forms/SpeakerContactForm'
import MentorContactForm from '@/components/forms/MentorContactForm'
import PartnerContactForm from '@/components/forms/PartnerContactForm'
import OtherContactForm from '@/components/forms/OtherContactForm'

export default {
  name: 'Contact',
  components: {
    SpeakerContactForm,
    MentorContactForm,
    PartnerContactForm,
    OtherContactForm
  },
  data () {
    return {
      selected: null,
      options: [
        { value: null, text: 'Please select an option' },
        { value: 'SpeakerContactForm', text: 'I am interested in being a guest speaker at a club meeting' },
        { value: 'MentorContactForm', text: 'I am interested in mentoring a group project' },
        { value: 'PartnerContactForm', text: 'I represent an organization that is interested in a partnership with the club' },
        { value: 'OtherContactForm', text: 'None of the above apply to me' }
      ]
    }
  }
}
</script>

<style scoped>

</style>
