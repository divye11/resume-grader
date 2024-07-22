"use client"
import LoadingState from "./LoadingState"
import Sidebar from "./Sidebar"
import { useEffect, useState } from "react"
import Jobs from "./Jobs"
import Header from "./Header"
import useApi from "../../hooks/useApi"

export function HomePage() {
  const { data, loading, makeRequest } = useApi<JobsList>()

  useEffect(() => {
    makeRequest({
      url: "jobs",
      method: "GET",
    })
  }, [])

  return (
    <div className="flex min-h-screen bg-muted/40">
      <Sidebar />
      <div className="flex-1 pl-0 sm:pl-64">
        <Header />
        <main className="p-4 sm:p-6">
          <div className="grid gap-6">
            {loading ? (
              Array.from({ length: 4 }).map((_, index) => (
                <LoadingState key={index} />
              ))
            ) : (
              <Jobs jobData={data?.jobs || []} />              
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

