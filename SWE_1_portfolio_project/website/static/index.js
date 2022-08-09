function deletePile() {fetch("/delete-pile",
    {method: "POST",
        }).then((_res) => {
    window.location.href = "/";
  });
}