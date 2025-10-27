{ pkgs, ... }: {
  channel = "stable-25.05";

  packages = [
    pkgs.nodejs_24
  ];

  services.mongodb = {
    enable = true;
  };

  idx = {
    extensions = [
      "mongodb.mongodb-vscode"
    ];

    workspace = {
      onCreate = {
        npm-install = "npm install";
        default.openFiles = [
          "index.js"
          "README.md"
        ];
      };
      onStart = {
        start-database = "mongod --port 27017 --fork --logpath ./.idx/database.log --dbpath ./.idx/.data";
      };
    };

    previews = {
      enable = true;
      previews = { };
    };
  };
}
