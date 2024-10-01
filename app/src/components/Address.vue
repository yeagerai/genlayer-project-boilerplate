<template>
  <span :title="fullAddress">{{ shortenedAddress }}</span>
</template>

<script>
export default {
  name: "Address",
  props: {
    address: {
      type: String,
      required: true,
    },
    maxLength: {
      type: Number,
      default: 12,
    },
  },
  computed: {
    fullAddress() {
      return this.address;
    },
    shortenedAddress() {
      if (!this.address) {
        return "";
      }
      if (this.address.length <= this.maxLength) {
        return this.address;
      }

      const halfLength = Math.floor((this.maxLength - 3) / 2);
      const start = this.address.slice(0, halfLength);
      const end = this.address.slice(-halfLength);

      return `${start}...${end}`;
    },
  },
};
</script>
