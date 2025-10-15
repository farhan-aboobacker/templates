{ pkgs, bundleid ? "com.example", ... }: {
  # Define an environment configuration
  # `pkgs` provides access to Nix packages
  # `bundleid` is an optional argument with a default value "com.example"
 
  # List of packages that should be available inside this environment
  packages = [
    pkgs.git      # Git - required for cloning or version control
    pkgs.glibc    # GNU C Library - common dependency for many binaries
    pkgs.which    # 'which' command - used to find the path of executables
  ];
 
  # Bootstrap script: runs automatically after the environment is built
  bootstrap = ''
   
    # Create a new Flutter project inside the output directory ($out)
    # --org specifies the package/bundle identifier (e.g., com.example)
    # --platforms defines which platforms to generate (web + android here)
    flutter create "$out" --org=${bundleid} --platforms="web,android"
 
    # Create a hidden folder ".idx" in the project for environment configs
    mkdir -p "$out/.idx"
 
    # Copy the current dev.nix file into the .idx directory inside the project
    # `${./dev.nix}` refers to a local file relative to this Nix script
    cp ${./dev.nix} "$out"/.idx/dev.nix
 
    # Ensure the output directory has proper write permissions for the user
    chmod -R u+w "$out"
  '';
}