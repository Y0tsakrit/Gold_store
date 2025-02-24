export default function SignInPage() {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 >Sign in</h1>
            <form className="flex flex-col gap-10">
                <label>
                    Email
                    <input type="email" />
                </label>
                <label>
                    Password
                    <input type="password" />
                </label>
                <button type="submit">Sign in</button>
            </form>
        </div>
    )
}