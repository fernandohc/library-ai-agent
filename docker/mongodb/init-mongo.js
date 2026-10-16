db = db.getSiblingDB("library_ai");

db.createUser({
  user: "library_app",
  pwd: "library_app_password",
  roles: [
    {
      role: "readWrite",
      db: "library_ai",
    },
  ],
});
