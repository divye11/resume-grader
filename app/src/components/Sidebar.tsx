import React from 'react';
import Link from "next/link"
import { BriefcaseIcon, BookmarkIcon } from './icons';


const Sidebar: React.FC = () => {
   return (
      <aside className="fixed inset-y-0 left-0 z-10 hidden w-64 flex-col border-r bg-background sm:flex">
         <div className="flex h-14 items-center border-b px-6">
            <h1 className="text-xl font-semibold">Job Ananlyzer</h1>
         </div>
         <nav className="flex-1 space-y-1 px-4 py-6">
            <Link
               href="#"
               className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
               prefetch={false}
            >
               <BriefcaseIcon className="h-5 w-5" />
               All Jobs
            </Link>
            <Link
               href="#"
               className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
               prefetch={false}
            >
               <BookmarkIcon className="h-5 w-5" />
               Saved Jobs
            </Link>
         </nav>
      </aside>
   );
};

export default Sidebar;