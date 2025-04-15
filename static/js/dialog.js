; (function () {

    const modal1 = new bootstrap.Modal(document.getElementById("edit_modal"))

    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "edit_dialog") {
        modal1.show()
      }
    })

    htmx.on("htmx:beforeSwap", (e) => {
      // Empty response targeting #dialog => hide the modal
      if (e.detail.target.id == "edit_dialog" && !e.detail.xhr.response) {
        modal1.hide()
        e.detail.shouldSwap = false
      }
    })

    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("edit_dialog").innerHTML = ""
    })
  })()

; (function () {

  const modal2 = new bootstrap.Modal(document.getElementById("remove_modal"))

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "remove_dialog") {
      modal2.show()
    }
  })

  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "remove_dialog" && !e.detail.xhr.response) {
      modal2.hide()
      e.detail.shouldSwap = false
    }
  })

  // Remove dialog content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("remove_dialog").innerHTML = ""
  })
})()


  