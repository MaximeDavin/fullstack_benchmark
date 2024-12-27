const Navbar = () => {
  return (
    <nav className="bg-purple-950 text-gray-300 shadow-md">
      <div className="flex items-center justify-between px-4 py-2">
        <div className="flex items-center justify-between">
          <Logo />
          <Menu />
        </div>
        <User />
      </div>
    </nav>
  );
};

const Logo = () => (
  <div className="text-2xl font-bold">
    <a href="/">Benchboxd</a>
  </div>
);

const Menu = () => (
  <ul className="flex space-x-6 px-8">
    <li>
      <a href="/movies" className="hover:text-white">
        Movies
      </a>
    </li>
    <li>
      <a href="/review" className="hover:text-white">
        Reviews
      </a>
    </li>
  </ul>
);

type UserProps = {
  username?: string;
};

const User = ({ username }: UserProps) => (
  <a href="/review" className="hover:text-white">
    {username ?? "Login"}
  </a>
);

export default Navbar;
