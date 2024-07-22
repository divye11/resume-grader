import React from 'react';
import {Input} from '@/components/ui/input';

const Header: React.FC = () => {
   return (
      <header className="sticky top-0 z-20 bg-background px-4 py-3 sm:px-6 sm:py-4">
         <div className="flex items-center justify-between">
            <h1 className="text-xl font-semibold">Jobs</h1>
            <div className="relative flex-1 sm:max-w-md">
               <div className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
               <Input
                  type="search"
                  placeholder="Search jobs..."
                  className="w-full rounded-md bg-muted pl-8 pr-4 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
               />
            </div>
         </div>
      </header>
   );
};

export default Header;