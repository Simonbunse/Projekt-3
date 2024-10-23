import Link from "next/link";
import { useRouter } from "next/router";
export default function Nav({show}) {
    const inactiveLink = 'flex gap-1 p-1 bg-white text-black text-xl rounded-sm';
    const activeLink = inactiveLink+' bg-green-300 rounded-sm';
    const inactiveIcon = ' size-8';
    const activeIcon = inactiveIcon+ ' rounded-sm text-primary'
    const router = useRouter();
    const {pathname} = router;

    return (
        <aside className={(show?'left-0':'-left-full')+" top-0 text-gray-500 p-4 fixed w-full bg-gray-300 h-full md:static md:w-auto transition-all rounded-lg"}>
            <nav className="flex flex-col gap-2">
                <Link href={'/'} className={pathname === ('/') ? activeLink : inactiveLink}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className={pathname === ('/') ? activeIcon : inactiveIcon}>
                        <path d="M11.47 3.841a.75.75 0 0 1 1.06 0l8.69 8.69a.75.75 0 1 0 1.06-1.061l-8.689-8.69a2.25 2.25 0 0 0-3.182 0l-8.69 8.69a.75.75 0 1 0 1.061 1.06l8.69-8.689Z" />
                        <path d="m12 5.432 8.159 8.159c.03.03.06.058.091.086v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 0 1-.75-.75v-4.5a.75.75 0 0 0-.75-.75h-3a.75.75 0 0 0-.75.75V21a.75.75 0 0 1-.75.75H5.625a1.875 1.875 0 0 1-1.875-1.875v-6.198a2.29 2.29 0 0 0 .091-.086L12 5.432Z" />
                    </svg>

                    Dashboard
                </Link>
                <Link href={'/parkinglot'} className={pathname.includes('/parkinglot') ? activeLink : inactiveLink}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className={pathname.includes('/parkinglot') ? activeIcon : inactiveIcon}>
                        <path d="M3.375 3C2.339 3 1.5 3.84 1.5 4.875v.75c0 1.036.84 1.875 1.875 1.875h17.25c1.035 0 1.875-.84 1.875-1.875v-.75C22.5 3.839 21.66 3 20.625 3H3.375Z" />
                        <path fillRule="evenodd" d="m3.087 9 .54 9.176A3 3 0 0 0 6.62 21h10.757a3 3 0 0 0 2.995-2.824L20.913 9H3.087Zm6.163 3.75A.75.75 0 0 1 10 12h4a.75.75 0 0 1 0 1.5h-4a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
                    </svg>

                    Parking Lot 1
                </Link>
                <Link href={'/parkinglot2'} className={pathname.includes('/parkinglot2') ? activeLink : inactiveLink}>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className={pathname.includes('/parkinglot2') ? activeIcon : inactiveIcon}>
                        <path d="M3.375 3C2.339 3 1.5 3.84 1.5 4.875v.75c0 1.036.84 1.875 1.875 1.875h17.25c1.035 0 1.875-.84 1.875-1.875v-.75C22.5 3.839 21.66 3 20.625 3H3.375Z" />
                        <path fillRule="evenodd" d="m3.087 9 .54 9.176A3 3 0 0 0 6.62 21h10.757a3 3 0 0 0 2.995-2.824L20.913 9H3.087Zm6.163 3.75A.75.75 0 0 1 10 12h4a.75.75 0 0 1 0 1.5h-4a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
                    </svg>

                    Parking Lot 2
                </Link>
            </nav>
        </aside>
    );
}