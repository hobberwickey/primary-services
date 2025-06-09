const apiRoot =
  process.env.NODE_ENV === "production"
    ? "https://api.deadlykitten.com"
    : "http://127.0.0.1:5000";

console.log("API ROOT:", apiRoot);
export const getTowns = () =>
  fetch(`${apiRoot}/municipalities/towns`).then((response) => response.json());

export const getTown = (town_id) =>
  fetch(`${apiRoot}/town/${town_id}`).then((response) => response.json());

export const getTownOffices = (town_id) =>
  fetch(`${apiRoot}/town/${town_id}/offices`).then((response) =>
    response.json(),
  );

export const getTownRequirements = (town_id) =>
  fetch(`${apiRoot}/town/${town_id}/requirements`).then((response) =>
    response.json(),
  );

export const createOffice = (args) => {
  let { municipality_id, office } = args;
  // return fetch(`http://127.0.0.1:5000/municipality/${municipality_id}/office`, {
  return fetch(`${apiRoot}/office`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ...office, municipality_id: municipality_id }),
  }).then((resp) => {
    return resp.json();
  });
};

export const createElection = (args) => {
  let { municipality_id, election } = args;

  return fetch(`${apiRoot}/election`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ...election, municipality_id: municipality_id }),
  }).then((resp) => {
    return resp.json();
  });
};

export const createRequirement = (town, requirement) =>
  fetch(`${apiRoot}/requirement`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ...requirement, municipality_id: town.id }),
  }).then((resp) => {
    return resp.json();
  });

//////////// Seat Separation /////////////

export const getMunicipality = (municipality_id) =>
  fetch(`${apiRoot}/municipality/${municipality_id}`).then((response) =>
    response.json(),
  );

export const getMunicipalityOffices = (municipality_id) =>
  fetch(`${apiRoot}/municipalities/${municipality_id}/offices`).then(
    (response) => response.json(),
  );

export const getMunicipalityElections = (municipality_id) =>
  fetch(`${apiRoot}/municipalities/${municipality_id}/elections`).then(
    (response) => response.json(),
  );

export const getMunicipalityCollections = (municipality_id) =>
  fetch(`${apiRoot}/municipalities/${municipality_id}/collections`).then(
    (response) => response.json(),
  );
