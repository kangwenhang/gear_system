import { reactive } from 'vue'

export const sharedStore = reactive({
  pulleys: [],
  beltParams: {
    flat_to_pitch: null,
    pitch_to_effective: null
  },
  calcTrigger: 0,
  formInfo: {
    fileNo: '',
    customer: '',
    project: '',
    cylinders: '',
    power: '',
    updateDesc: '',
    issueDesc: '',
    version: 1
  },
  tensioner: null,
  beltFullParams: null,
  loadData: [],
  alignmentResult: [],
  alignmentInput: {
    centerHeight: 0,
    perpendicularity: 0
  },
  showReport: false
})
