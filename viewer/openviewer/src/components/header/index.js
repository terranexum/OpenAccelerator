import { h } from 'preact';
import { Link } from 'preact-router/match';
import style from './style.css';

const Header = () => (
	<header class={style.header}>
		<a href="/" class={style.logo}>
			<img src="../../assets/tn_logo_circle.png" alt="TerraNexum Logo" height="64" width="64" />
			<h1>OpenAccelerator</h1>
		</a>
		
		<nav>
			<Link activeClassName={style.active} href="/">
				Home
			</Link>
			<Link activeClassName={style.active} href="/github">
				GitHub
			</Link>
			<Link activeClassName={style.active} href="/github/oa">
				OpenAccelerator Projects
			</Link>
		</nav>
	</header>
);

export default Header;
